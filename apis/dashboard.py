"""API routes for study redcap"""

from typing import Any, Dict, List, Union

from flask import request
from flask_restx import Namespace, Resource, fields
from jsonschema import ValidationError, validate

import caching
import model
from modules.etl import ModuleTransform, RedcapLiveTransform, RedcapReleaseTransform
from modules.etl.config import (
    moduleTransformConfigs,
    redcapLiveTransformConfig,
    redcapReleaseTransformConfig,
)

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

redcap_project_dashboard_module_model = api.model(
    "RedcapProjectDashboardModule",
    {
        "name": fields.String(
            required=True, readonly=True, description="Dashboard module name"
        ),
        "id": fields.String(
            required=True, readonly=True, description="Dashboard module ID"
        ),
        "report_key": fields.String(
            required=True,
            readonly=True,
            description="Dashboard module associated REDCap report key",
        ),
        "selected": fields.Boolean(
            required=True, readonly=True, description="Dashboard module is selected"
        ),
        "public": fields.Boolean(
            required=True,
            readonly=True,
            description="Dashboard module is publicly available",
        ),
        "visualizations": fields.List(
            fields.Nested(visualization_model),
            required=True,
            readonly=True,
            description="Visualizations",
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
        "report_has_modules": fields.Boolean(
            required=True,
            readonly=True,
            description="REDCap report is associated with one or more dashboard modules",
        ),
        "public": fields.Boolean(
            required=True,
            readonly=True,
            description="Dashboard module is publicly available",
        ),
    },
)

redcap_project_dashboard_model = api.model(
    "RedcapProjectDashboard",
    {
        "redcap_id": fields.String(
            required=True, readonly=True, description="REDCap ID"
        ),
        "id": fields.String(
            required=True, readonly=True, description="REDCap dashboard ID"
        ),
        "name": fields.String(
            required=True, readonly=True, description="REDCap dashboard name"
        ),
        "redcap_pid": fields.String(
            required=True, readonly=True, description="REDCap project ID (PID)"
        ),
        "reports": fields.List(
            fields.Nested(
                redcap_project_report_model,
                required=True,
                readonly=True,
                description="Associated REDCap reports",
            )
        ),
        "modules": fields.List(
            fields.Nested(
                redcap_project_dashboard_module_model,
                required=True,
                readonly=True,
                description="REDCap dashboard module",
            )
        ),
        "public": fields.Boolean(
            required=True, readonly=True, description="Is this REDCap dashboard public?"
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
            required=True, readonly=True, description="Dashboard module ID"
        ),
        "redcap_pid": fields.String(
            required=True, readonly=True, description="REDCap project ID (PID)"
        ),
        "report_key": fields.String(
            required=True,
            readonly=True,
            description="Dashboard module associated REDCap report key",
        ),
        "selected": fields.Boolean(
            required=True, readonly=True, description="Dashboard module is selected"
        ),
        "public": fields.Boolean(
            required=True,
            readonly=True,
            description="Dashboard module is publicly available",
        ),
    },
)
redcap_project_dashboard_connector_model = api.model(
    "RedcapProjectDashboardConnector",
    {
        "redcap_id": fields.String(
            required=True, readonly=True, description="REDCap ID"
        ),
        "redcap_pid": fields.String(
            required=True, readonly=True, description="REDCap project ID (PID)"
        ),
        "reports": fields.List(
            fields.Nested(
                redcap_project_report_model,
                required=True,
                readonly=True,
                description="Associated REDCap reports",
            )
        ),
        "id": fields.String(
            required=True, readonly=True, description="REDCap dashboard ID"
        ),
        "name": fields.String(
            required=True, readonly=True, description="REDCap dashboard name"
        ),
        "modules": fields.List(
            fields.Nested(
                redcap_project_dashboard_module_connector_model,
                required=True,
                readonly=True,
                description="REDCap dashboard module connector",
            )
        ),
        "public": fields.Boolean(
            required=True, readonly=True, description="Is this REDCap dashboard public?"
        ),
    },
)


@api.route("/study/<study_id>/dashboard")
class RedcapProjectDashboards(Resource):
    @api.doc("Get all study dashboards")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model, as_list=True)
    def get(self, study_id: str):
        """Get all REDCap project dashboards"""
        study = model.db.session.query(model.Study).get(study_id)
        if not is_granted("view", study):
            return "Access denied, you can not view", 403
        redcap_project_dashboards_query = model.StudyDashboard.query.filter_by(
            study=study
        )
        redcap_project_dashboards: List[Dict[str, Any]] = [
            redcap_project_dashboard.to_dict()
            for redcap_project_dashboard in redcap_project_dashboards_query
        ]
        return redcap_project_dashboards, 201

    @api.doc("Create a new study dashboard")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def post(self, study_id: str):
        """Create REDCap project dashboard"""
        study = model.Study.query.get(study_id)
        if not is_granted("add_dashboard", study):
            return "Access denied, you can not create", 403
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "redcap_id",
                "redcap_pid",
                "reports",
                "name",
                "modules",
                "public",
            ],
            "properties": {
                "redcap_id": {"type": "string", "minLength": 1},
                "redcap_pid": {"type": "string", "minLength": 1},
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
                                    "report_has_modules": {"type": "boolean"},
                                    "public": {"type": "boolean"},
                                },
                            }
                        ]
                    },
                    "minItems": 1,
                },
                "name": {"type": "string", "minLength": 1},
                "modules": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string", "minLength": 1},
                                    "name": {"type": "string", "minLength": 1},
                                    "selected": {"type": "boolean"},
                                    "public": {"type": "boolean"},
                                    "report_key": {"type": "string", "minLength": 1},
                                },
                            }
                        ]
                    },
                    "minItems": 1,
                },
                "public": {"type": "boolean"},
            },
        }
        data: Union[Any, Dict[str, Any]] = request.json
        print(data)
        try:
            validate(request.json, schema)
        except ValidationError as e:
            print("validation error")
            return e.message, 400
        if len(data["redcap_id"]) < 1:
            return (
                f"""redcap redcap_id is required to connect a dashboard:
                {data['redcap_id']}""",
                400,
            )
        if len(data["redcap_pid"]) < 1:
            return (
                f"""redcap redcap_pid is required to connect a dashboard:
                {data['redcap_pid']}""",
                400,
            )
        if len(data["reports"]) < 1:
            return (
                f"""redcap reports are required to connect a dashboard:
                {data['reports']}""",
                400,
            )
        if len(data["name"]) < 1:
            return (
                f"""dashboard name is required to connect a dashboard:
                {data['name']}""",
                400,
            )
        if len(data["modules"]) < 1:
            return (
                f"""dashboard modules is required to connect a dashboard:
                {data['modules']}""",
                400,
            )

        if not isinstance(data["public"], bool):
            return (
                f"""public must be a Boolean to connect a dashboard:
                {data['public']}""",
                400,
            )
        connect_redcap_project_dashboard_data = model.StudyDashboard.from_data(
            study, data
        )
        model.db.session.add(connect_redcap_project_dashboard_data)
        model.db.session.commit()
        connect_redcap_project_dashboard: Dict[
            str, Any
        ] = connect_redcap_project_dashboard_data.to_dict()
        return connect_redcap_project_dashboard, 201


@api.route("/study/<study_id>/dashboard/<dashboard_id>/connector")
class RedcapProjectDashboardConnector(Resource):
    @api.doc("Get a study dashboard connector")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_connector_model)
    def get(self, study_id: str, dashboard_id: str):
        """Get REDCap project dashboard connector"""
        study = model.db.session.query(model.Study).get(study_id)
        if not is_granted("view", study):
            return "Access denied, you can not view this dashboard connector", 403

        # Get Dashboard Connector
        redcap_project_dashboard_connector_query: Any = model.db.session.query(
            model.StudyDashboard
        ).get(dashboard_id)

        redcap_project_dashboard_connector: Dict[
            str, Any
        ] = redcap_project_dashboard_connector_query.to_dict()

        return redcap_project_dashboard_connector, 201


@api.route("/study/<study_id>/dashboard/<dashboard_id>")
class RedcapProjectDashboard(Resource):
    @api.doc("Get a study dashboard")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def get(self, study_id: str, dashboard_id: str):
        """Get REDCap project dashboard"""
        model.db.session.flush()
        study = model.db.session.query(model.Study).get(study_id)
        if not is_granted("view", study):
            return "Access denied, you can not view this dashboard", 403

        # Retrieve Dashboard Redis Cache if Available
        # cached_redcap_project_dashboard = caching.cache.get(
        #     f"$study_id#{study_id}$dashboard_id#{dashboard_id}"
        # )
        # if cached_redcap_project_dashboard is not None:
        #     return cached_redcap_project_dashboard, 201

        # Get Base Transform Config for ETL - Live
        transformConfig = redcapLiveTransformConfig

        # Query Project Dashboard by ID
        redcap_project_dashboard_query: Any = model.db.session.query(
            model.StudyDashboard
        ).get(dashboard_id)
        redcap_project_dashboard: Dict[
            str, Any
        ] = redcap_project_dashboard_query.to_dict()

        # Get REDCap Project
        redcap_id = redcap_project_dashboard["redcap_id"]
        redcap_project_view_query: Any = model.db.session.query(model.StudyRedcap).get(
            redcap_id
        )
        redcap_project_view: Dict[str, Any] = redcap_project_view_query.to_dict()

        # Set report_ids for ETL
        report_keys = []
        for report in redcap_project_dashboard["reports"]:
            for i, report_config in enumerate(transformConfig["reports"]):
                if (
                    len(report["report_id"]) > 0
                    and report["report_key"] == report_config["key"]
                ):
                    report_keys.append(report["report_key"])
                    transformConfig["reports"][i]["kwdargs"]["report_id"] = report[
                        "report_id"
                    ]

        # Remove Unused Reports
        transformConfig["reports"] = [
            report
            for report in redcapLiveTransformConfig["reports"]
            if report["key"] in report_keys
        ]

        # Set Post Transform Merge
        index_columns, post_transform_merges = transformConfig["post_transform_merge"]
        transformConfig["post_transform_merge"] = (
            index_columns,
            [
                (report_key, transform_kwdargs)
                for report_key, transform_kwdargs in post_transform_merges
                if report_key in report_keys
            ],
        )

        # Set REDCap API Config
        transformConfig["redcap_api_url"] = redcap_project_view["api_url"]
        transformConfig["redcap_api_key"] = redcap_project_view["api_key"]

        # Finalize ETL Config
        redcap_etl_config = transformConfig

        redcapTransform = RedcapLiveTransform(redcap_etl_config)

        # Execute Dashboard Module Transforms
        for dashboard_module in redcap_project_dashboard["modules"]:
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
        caching.cache.set(
            f"$study_id#{study_id}$dashboard_id#{dashboard_id}",
            redcap_project_dashboard,
        )

        return redcap_project_dashboard, 201

    @api.doc("Update a study dashboard")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def put(self, study_id: str, dashboard_id: str):
        """Update REDCap project dashboard"""
        study = model.db.session.query(model.Study).get(study_id)
        if not is_granted("update_dashboard", study):
            return "Access denied, you can not modify this dashboard", 403
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "redcap_id",
                "redcap_pid",
                "reports",
                "dashboard_id",
                "name",
                "modules",
            ],
            "properties": {
                "redcap_id": {"type": "string", "minLength": 1},
                "redcap_pid": {"type": "string", "minLength": 1},
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
                                    "report_has_modules": {"type": "boolean"},
                                    "public": {"type": "boolean"},
                                },
                            }
                        ]
                    },
                    "minItems": 1,
                },
                "dashboard_id": {"type": "string", "minLength": 1},
                "name": {"type": "string", "minLength": 1},
                "modules": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string", "minLength": 1},
                                    "name": {"type": "string", "minLength": 1},
                                    "selected": {"type": "boolean"},
                                    "public": {"type": "boolean"},
                                    "report_key": {"type": "string", "minLength": 1},
                                },
                            }
                        ]
                    },
                    "minItems": 1,
                },
                "public": {"type": "boolean"},
            },
        }
        data: Union[Any, Dict[str, Any]] = request.json
        try:
            validate(request.json, schema)
        except ValidationError as e:
            print("validation error")
            return e.message, 400
        if len(data["redcap_id"]) < 1:
            return (
                f"""redcap redcap_id is required to connect a dashboard:
                {data['redcap_id']}""",
                400,
            )
        if len(data["redcap_pid"]) < 1:
            return (
                f"""redcap redcap_pid is required to connect a dashboard:
                {data['redcap_pid']}""",
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
        if len(data["name"]) < 1:
            return (
                f"""dashboard name is required to connect a dashboard:
                {data['name']}""",
                400,
            )
        if len(data["modules"]) < 1:
            return (
                f"""dashboard modules is required to connect a dashboard:
                {data['name']}""",
                400,
            )
        if not isinstance(data["public"], bool):
            return (
                f"""public must be a Boolean to connect a dashboard:
                {data['public']}""",
                400,
            )

        redcap_project_dashboard_query = model.StudyDashboard.query.get(dashboard_id)
        if redcap_project_dashboard_query is None:
            return "An error occurred while updating the dashboard", 500

        redcap_project_dashboard_query.update(data)
        model.db.session.commit()
        update_redcap_project_dashboard: Dict[
            str, Any
        ] = redcap_project_dashboard_query.to_dict()

        # Clear Dashboard from Redis Cache
        caching.cache.delete(f"$study_id#{study_id}$dashboard_id#{dashboard_id}")

        return update_redcap_project_dashboard, 201

    @api.doc("Delete a study dashboard")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def delete(self, study_id: str, dashboard_id: str):
        """Delete REDCap project dashboard"""
        study = model.Study.query.get(study_id)
        if not is_granted("delete_dashboard", study):
            return "Access denied, you can not delete this dashboard", 403

        model.StudyDashboard.query.filter_by(id=dashboard_id).delete()
        model.db.session.commit()

        return 204


@api.route("/study/<study_id>/dashboard/public")
class RedcapProjectDashboardPublic(Resource):
    @api.doc("Get the public study dashboard")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def get(self, study_id: str):
        """Get REDCap project dashboard"""
        model.db.session.flush()
        study = model.db.session.query(model.Study).get(study_id)
        # if not is_granted("view", study):
        #     return "Access denied, you can not view this dashboard", 403

        # Get Dashboard
        redcap_project_dashboards_query = model.StudyDashboard.query.filter_by(
            study=study, public=True
        )
        #  List of Dashboards
        redcap_project_dashboards: List[Dict[str, Any]] = [
            redcap_project_dashboard.to_dict()
            for redcap_project_dashboard in redcap_project_dashboards_query
        ]
        # There Should Only Be One, Pop it From The List If It's There
        if len(redcap_project_dashboards) > 0:
            redcap_project_dashboard = redcap_project_dashboards.pop()
        else:
            return "No public dashboard found", 404

        # Public Dashboard ID
        dashboard_id = redcap_project_dashboard["id"]

        # Retrieve Dashboard Redis Cache if Available
        # cached_redcap_project_dashboard = caching.cache.get(
        #     f"$study_id#{study_id}$dashboard_id#{dashboard_id}#public"
        # )
        # if cached_redcap_project_dashboard is not None:
        #     return cached_redcap_project_dashboard, 201

        #
        # No Cache, Do ETL
        #

        # Get Base Transform Config for ETL - Release
        transformConfig = redcapReleaseTransformConfig

        # Set report_ids for ETL
        report_keys = []
        for report in redcap_project_dashboard["reports"]:
            for i, report_config in enumerate(transformConfig["reports"]):
                if (
                    len(report["report_id"]) > 0
                    and report["report_key"] == report_config["key"]
                ):
                    report_keys.append(report["report_key"])
                    transformConfig["reports"][i]["kwdargs"]["report_id"] = report[
                        "report_id"
                    ]

        # Remove Unused Reports
        transformConfig["reports"] = [
            report
            for report in redcapLiveTransformConfig["reports"]
            if report["key"] in report_keys
        ]

        # Set Post Transform Merge
        index_columns, post_transform_merges = transformConfig["post_transform_merge"]
        transformConfig["post_transform_merge"] = (
            index_columns,
            [
                (report_key, transform_kwdargs)
                for report_key, transform_kwdargs in post_transform_merges
                if report_key in report_keys
            ],
        )

        # Finalize ETL Config
        redcap_etl_config = transformConfig

        # Execute REDCap Release ETL
        redcapTransform = RedcapReleaseTransform(redcap_etl_config)

        # Execute Dashboard Module Transforms
        for dashboard_module in redcap_project_dashboard["modules"]:
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
        caching.cache.set(
            f"$study_id#{study_id}$dashboard_id#{dashboard_id}#public",
            redcap_project_dashboard,
        )

        return redcap_project_dashboard, 201
