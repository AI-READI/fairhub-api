"""API routes for study redcap"""

from typing import Any, Dict, List, Union

from flask import request

# from flask_caching import Cache
from flask_restx import Namespace, Resource, fields, reqparse
from jsonschema import ValidationError, validate

import model
from caching import cache
from modules.etl import ModuleTransform, RedcapTransform
from modules.etl.config import moduleTransformConfigs, redcapTransformConfig

from .authentication import is_granted

api = Namespace("Dashboard", description="Dashboard operations", path="/")

datum_model = api.model(
    "Datum",
    {
        "filterby": fields.String(
            required=True, readonly=True, description="Filterby field"
        ),
        "group": fields.String(required=True, readonly=True, description="Group field"),
        "subgroup": fields.String(
            required=False, readonly=True, description="Subgroup field"
        ),
        "value": fields.Raw(required=False, readonly=True, description="Value field"),
        "x": fields.Raw(required=False, readonly=True, description="X-axis field"),
        "y": fields.Float(required=False, readonly=True, description="Y-axis field"),
        "datetime": fields.String(
            required=False, readonly=True, description="Date field"
        ),
    },
)

visualization_model = api.model(
    "Visualization",
    {
        "id": fields.String(
            required=True, readonly=True, description="Visualization ID"
        ),
        "data": fields.List(
            fields.Nested(datum_model),
            required=True,
            readonly=True,
            description="Visualization data",
        ),
    },
)

redcap_project_report_model = api.model(
    "RedcapProjectReport",
    {
        "report_id": fields.String(
            required=True, readonly=True, description="REDCap report ID"
        ),
        "report_key": fields.String(
            required=True, readonly=True, description="REDCap report key"
        ),
        "report_name": fields.String(
            required=True, readonly=True, description="REDCap report name"
        ),
    },
)

redcap_project_dashboard_module_model = api.model(
    "RedcapProjectDashboardModule",
    {
        "name": fields.String(
            required=True, readonly=True, description="Dashboard module name"
        ),
        "id": fields.String(
            required=True, readonly=True, description="Dashboard module id"
        ),
        "report_key": fields.String(
            required=True,
            readonly=True,
            description="Dashboard module associated REDCap report key",
        ),
        "selected": fields.Boolean(
            required=True, readonly=True, description="Dashboard module is selected"
        ),
        "visualizations": fields.List(
            fields.Nested(visualization_model),
            required=True,
            readonly=True,
            description="Visualizations",
        ),
    },
)
redcap_project_dashboard_model = api.model(
    "RedcapProjectDashboard",
    {
        "project_id": fields.String(
            required=True, readonly=True, description="REDCap project ID (pid)"
        ),
        "reports": fields.List(
            fields.Nested(
                redcap_project_report_model,
                required=True,
                readonly=True,
                description="Associated REDCap reports",
            )
        ),
        "dashboard_id": fields.String(
            required=True, readonly=True, description="REDCap dashboard ID"
        ),
        "dashboard_name": fields.String(
            required=True, readonly=True, description="REDCap dashboard name"
        ),
        "dashboard_modules": fields.List(
            fields.Nested(
                redcap_project_dashboard_module_model,
                required=True,
                readonly=True,
                description="REDCap dashboard module",
            )
        ),
    },
)
redcap_project_dashboard_module_connector_model = api.model(
    "RedcapProjectDashboardModuleConnector",
    {
        "name": fields.String(
            required=True, readonly=True, description="Dashboard module name"
        ),
        "id": fields.String(
            required=True, readonly=True, description="Dashboard module id"
        ),
        "report_key": fields.String(
            required=True,
            readonly=True,
            description="Dashboard module associated REDCap report key",
        ),
        "selected": fields.Boolean(
            required=True, readonly=True, description="Dashboard module is selected"
        ),
    },
)
redcap_project_dashboard_connector_model = api.model(
    "RedcapProjectDashboardConnector",
    {
        "project_id": fields.String(
            required=True, readonly=True, description="REDCap project ID (pid)"
        ),
        "reports": fields.List(
            fields.Nested(
                redcap_project_report_model,
                required=True,
                readonly=True,
                description="Associated REDCap reports",
            )
        ),
        "dashboard_id": fields.String(
            required=True, readonly=True, description="REDCap dashboard ID"
        ),
        "dashboard_name": fields.String(
            required=True, readonly=True, description="REDCap dashboard name"
        ),
        "dashboard_modules": fields.List(
            fields.Nested(
                redcap_project_dashboard_module_connector_model,
                required=True,
                readonly=True,
                description="REDCap dashboard module connector",
            )
        ),
    },
)

# Parser
dashboard_parser = reqparse.RequestParser()
dashboard_parser.add_argument("dashboard_id", type=str, help="Dashboard ID")


@api.route("/study/<study_id>/dashboard/all")
class RedcapProjectDashboards(Resource):
    @api.doc("redcap_project_dashboards")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model, as_list=True)
    def get(self, study_id: int):
        """Get all REDCap project dashboards"""
        study = model.db.session.query(model.Study).get(study_id)
        if is_granted("viewer", study):
            return "Access denied, you can not modify", 403
        redcap_project_dashboards_query = (
            model.StudyRedcapProjectDashboard.query.filter_by(study=study)
        )
        redcap_project_dashboards: List[Dict[str, Any]] = [
            redcap_project_dashboard.to_dict()
            for redcap_project_dashboard in redcap_project_dashboards_query
        ]
        return redcap_project_dashboards, 201


@api.route("/study/<study_id>/dashboard/add")
class AddRedcapProjectDashboard(Resource):
    @api.doc(parser=dashboard_parser)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def post(self, study_id: int):
        """Create REDCap project dashboard"""
        study = model.Study.query.get(study_id)
        if is_granted("add_dashboard", study):
            return "Access denied, you can not modify", 403
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "project_id",
                "reports",
                "dashboard_name",
                "dashboard_modules",
            ],
            "properties": {
                "project_id": {"type": "string", "minLength": 1},
                "reports": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "report_id": {"type": "string", "minLength": 0},
                                    "report_key": {"type": "string", "minLength": 1},
                                    "report_name": {"type": "string", "minLength": 1},
                                },
                            }
                        ]
                    },
                    "minItems": 1,
                },
                "dashboard_name": {"type": "string", "minLength": 1},
                "dashboard_modules": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string", "minLength": 1},
                                    "name": {"type": "string", "minLength": 1},
                                    "selected": {"type": "boolean"},
                                    "report_key": {"type": "string", "minLength": 1},
                                },
                            }
                        ]
                    },
                    "minItems": 1,
                },
            },
        }
        data: Union[Any, Dict[str, Any]] = request.json
        try:
            validate(request.json, schema)
        except ValidationError as e:
            print("validation error")
            return e.message, 400
        if len(data["project_id"]) < 1:
            return (
                f"""redcap project_id is required to connect a dashboard:
                {data['project_id']}""",
                400,
            )
        if len(data["reports"]) < 1:
            return (
                f"""redcap reports are required to connect a dashboard:
                {data['reports']}""",
                400,
            )
        if len(data["dashboard_name"]) < 1:
            return (
                f"""dashboard dashboard_name is required to connect a dashboard:
                {data['dashboard_name']}""",
                400,
            )
        if len(data["dashboard_modules"]) < 1:
            return (
                f"""dashboard dashboard_modules is required to connect a dashboard:
                {data['dashboard_name']}""",
                400,
            )
        connect_redcap_project_dashboard_data = (
            model.StudyRedcapProjectDashboard.from_data(study, data)
        )
        model.db.session.add(connect_redcap_project_dashboard_data)
        model.db.session.commit()
        connect_redcap_project_dashboard: Dict[str, Any] = (
            connect_redcap_project_dashboard_data.to_dict()
        )
        return connect_redcap_project_dashboard, 201


@api.route("/study/<study_id>/dashboard-connector")
class RedcapProjectDashboardConnector(Resource):
    @api.doc(parser=dashboard_parser)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_connector_model)
    def get(self, study_id: int):
        """Get REDCap project dashboard connector"""
        study = model.db.session.query(model.Study).get(study_id)
        if is_granted("viewer", study):
            return "Access denied, you can not get this dashboard", 403

        # Get Dashboard Connector
        dashboard_id = dashboard_parser.parse_args()["dashboard_id"]
        redcap_project_dashboard_connector_query: Any = model.db.session.query(
            model.StudyRedcapProjectDashboard
        ).get(dashboard_id)

        redcap_project_dashboard_connector: Dict[str, Any] = (
            redcap_project_dashboard_connector_query.to_dict()
        )

        return redcap_project_dashboard_connector, 201


@api.route("/study/<study_id>/dashboard")
class RedcapProjectDashboard(Resource):
    @api.doc(parser=dashboard_parser)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def get(self, study_id: int):
        """Get REDCap project dashboard"""
        model.db.session.flush()
        study = model.db.session.query(model.Study).get(study_id)
        if is_granted("viewer", study):
            return "Access denied, you can not get this dashboard", 403

        # Get Dashboard
        dashboard_id = dashboard_parser.parse_args()["dashboard_id"]

        # Retrieve Dashboard Redis Cache
        cached_redcap_project_dashboard = cache.get(
            f"$study_id#{study_id}$dashboard_id#{dashboard_id}"
        )

        if cached_redcap_project_dashboard is not None:
            return cached_redcap_project_dashboard, 201

        redcap_project_dashboard_query: Any = model.db.session.query(
            model.StudyRedcapProjectDashboard
        ).get(dashboard_id)
        redcap_project_dashboard: Dict[str, Any] = (
            redcap_project_dashboard_query.to_dict()
        )

        # Get REDCap Project
        project_id = redcap_project_dashboard["project_id"]
        redcap_project_view_query: Any = model.db.session.query(
            model.StudyRedcapProjectApi
        ).get(project_id)
        redcap_project_view: Dict[str, Any] = redcap_project_view_query.to_dict()

        # Set report_ids for ETL
        for report in redcap_project_dashboard["reports"]:
            for i, report_config in enumerate(redcapTransformConfig["reports"]):
                if (
                    report["report_key"] == report_config["key"]
                    and len(report["report_id"]) > 0
                ):
                    redcapTransformConfig["reports"][i]["kwdargs"]["report_id"] = (
                        report["report_id"]
                    )

        # Structure REDCap ETL Config
        redcap_etl_config = {
            "redcap_api_url": redcap_project_view["project_api_url"],
            "redcap_api_key": redcap_project_view["project_api_key"],
        } | redcapTransformConfig

        redcapTransform = RedcapTransform(redcap_etl_config)

        # Execute Dashboard Module Transforms
        for dashboard_module in redcap_project_dashboard["dashboard_modules"]:
            if dashboard_module["selected"]:
                mergedTransform = redcapTransform.merged
                transform, module_etl_config = moduleTransformConfigs[
                    dashboard_module["id"]
                ]
                moduleTransform = ModuleTransform(module_etl_config)
                transformed = getattr(moduleTransform, transform)(
                    mergedTransform
                ).transformed
                dashboard_module["visualizations"] = {
                    "id": dashboard_module["id"],
                    "data": transformed,
                }
            else:
                dashboard_module["visualizations"] = {
                    "id": dashboard_module["id"],
                    "data": [],
                }

        # Create Dashboard Redis Cache
        cache.set(
            f"$study_id#{study_id}$dashboard_id#{dashboard_id}",
            redcap_project_dashboard,
        )

        return redcap_project_dashboard, 201


@api.route("/study/<study_id>/dashboard/edit")
class EditRedcapProjectDashboard(Resource):
    @api.doc(parser=dashboard_parser)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def put(self, study_id: int):
        """Update REDCap project dashboard"""
        study = model.db.session.query(model.Study).get(study_id)
        if is_granted("update_dashboard", study):
            return "Access denied, you can not modify this dashboard", 403
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "project_id",
                "reports",
                "dashboard_id",
                "dashboard_name",
                "dashboard_modules",
            ],
            "properties": {
                "project_id": {"type": "string", "minLength": 1},
                "reports": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "report_id": {"type": "string", "minLength": 0},
                                    "report_key": {"type": "string", "minLength": 1},
                                    "report_name": {"type": "string", "minLength": 1},
                                },
                            }
                        ]
                    },
                    "minItems": 1,
                },
                "dashboard_id": {"type": "string", "minLength": 1},
                "dashboard_name": {"type": "string", "minLength": 1},
                "dashboard_modules": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string", "minLength": 1},
                                    "name": {"type": "string", "minLength": 1},
                                    "selected": {"type": "boolean"},
                                    "report_key": {"type": "string", "minLength": 1},
                                },
                            }
                        ]
                    },
                    "minItems": 1,
                },
            },
        }
        data: Union[Any, Dict[str, Any]] = request.json
        try:
            validate(request.json, schema)
        except ValidationError as e:
            print("validation error")
            return e.message, 400
        if len(data["project_id"]) < 1:
            return (
                f"""redcap project_id is required to connect a dashboard:
                {data['project_id']}""",
                400,
            )
        if len(data["reports"]) < 1:
            return (
                f"""redcap reports are required to connect a dashboard:
                {data['reports']}""",
                400,
            )
        if len(data["dashboard_id"]) < 1:
            return (
                f"""dashboard dashboard_id is required to connect a dashboard:
                {data['dashboard_id']}""",
                400,
            )
        if len(data["dashboard_name"]) < 1:
            return (
                f"""dashboard dashboard_name is required to connect a dashboard:
                {data['dashboard_name']}""",
                400,
            )
        if len(data["dashboard_modules"]) < 1:
            return (
                f"""dashboard dashboard_modules is required to connect a dashboard:
                {data['dashboard_name']}""",
                400,
            )

        dashboard_id = data["dashboard_id"]

        redcap_project_dashboard_query = model.StudyRedcapProjectDashboard.query.get(
            dashboard_id
        )
        if redcap_project_dashboard_query is None:
            return "An error occurred while updating the dashboard", 500

        redcap_project_dashboard_query.update(data)
        model.db.session.commit()
        update_redcap_project_dashboard: Dict[str, Any] = (
            redcap_project_dashboard_query.to_dict()
        )

        # Clear Dashboard from Redis Cache
        cache.delete(f"$study_id#{study_id}$dashboard_id#{dashboard_id}")

        return update_redcap_project_dashboard, 201


@api.route("/study/<study_id>/dashboard/delete")
class DeleteRedcapProjectDashboard(Resource):
    @api.doc(parser=dashboard_parser)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def delete(self, study_id: int):
        """Delete REDCap project dashboard"""
        study = model.Study.query.get(study_id)
        if is_granted("delete_dashboard", study):
            return "Access denied, you can not delete this redcap project", 403

        dashboard_id = dashboard_parser.parse_args()["dashboard_id"]
        model.StudyRedcapProjectDashboard.query.filter_by(
            dashboard_id=dashboard_id
        ).delete()
        model.db.session.commit()

        return 204
