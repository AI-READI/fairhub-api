"""API routes for study redcap"""
from typing import Any, Union

from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from jsonschema import ValidationError, validate

import model

from .authentication import is_granted

api = Namespace("Dashboard", description="Dashboard operations", path="/")

redcap_project_dashboard_model = api.model(
    "RedcapProjectDashboard",
    {
        "study_id": fields.String(required=True, description="Study ID"),
        "project_id": fields.String(
            required=True, description="REDCap project ID (pid)"
        ),
        "dashboard_id": fields.String(
            required=True, readonly=True, description="REDCap dashboard ID"
        ),
        "dashboard_name": fields.String(
            required=True, readonly=True, description="REDCap dashboard name"
        ),
        "dashboard_modules": fields.String(
            required=True, readonly=True, description="REDCap dashboard name"
        ),
        "report_ids": fields.String(
            required=True, readonly=True, description="REDCap project report IDs"
        ),
    },
)

dashboard_parser = reqparse.RequestParser()
dashboard_parser.add_argument("dashboard_id", type=str, help="Dashboard ID")


@api.route("/study/<study_id>/dashboard/all")
class RedcapProjectDashboards(Resource):
    @api.doc("redcap_project_dashboards")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model, as_list=True)
    def get(self, study_id: int):
        """Get all study REDCap project dashboard"""
        study = model.db.session.query(model.Study).get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not modify", 403
        redcap_project_dashboards = model.StudyRedcapProjectDashboard.query.filter_by(
            study=study
        )
        redcap_project_dashboards = [
            redcap_project_dashboard.to_dict()
            for redcap_project_dashboard in redcap_project_dashboards
        ]
        return redcap_project_dashboards, 201


@api.route("/study/<study_id>/dashboard/connect")
class ConnectRedcapProjectDashboard(Resource):
    @api.doc(parser=dashboard_parser)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def post(self, study_id: int):
        """Create study REDCap project dashboard"""
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not modify", 403
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "project_id",
                "dashboard_name",
                "dashboard_modules",
            ],
            "properties": {
                "project_id": {"type": "string", "minLength": 1},
                "dashboard_name": {"type": "string", "minLength": 1},
                "dashboard_modules": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "key": {"type": "string", "minLength": 1},
                                    "name": {"type": "string", "minLength": 1},
                                    "selected": {"type": "boolean"},
                                    "reportId": {"type": "string", "minLength": 0},
                                },
                            }
                        ]
                    },
                    "minItems": 1,
                },
            },
        }
        data: Union[Any, dict] = request.json
        try:
            validate(request.json, schema)
        except ValidationError as e:
            print(e)
            return e.message, 400
        print("moduleslength", len(data["dashboard_modules"]))

        if len(data["project_id"]) < 1:
            return (
                f"redcap project_id is required to connect a dashboard: {data['project_id']}",
                400,
            )
        if len(data["dashboard_name"]) < 1:
            return (
                f"dashboard dashboard_name is required to connect a dashboard: {data['dashboard_name']}",
                400,
            )
        if len(data["dashboard_modules"]) < 1:
            return (
                f"dashboard dashboard_modules is required to connect a dashboard: {data['dashboard_name']}",
                400,
            )
        data["dashboard_modules"] = [
            dashboard_module
            for dashboard_module in data["dashboard_modules"]
            if dashboard_module["selected"]
        ]
        connect_redcap_project_dashboard = model.StudyRedcapProjectDashboard.from_data(
            study, data
        )
        model.db.session.add(connect_redcap_project_dashboard)
        model.db.session.commit()
        connect_redcap_project_dashboard = connect_redcap_project_dashboard.to_dict()
        return connect_redcap_project_dashboard, 201


@api.route("/study/<study_id>/dashboard")
class RedcapProjectDashboard(Resource):
    """Get study REDCap project dashboard"""

    @api.doc(parser=dashboard_parser)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def get(self, study_id: int):
        """Get Study Redcap Project Dashboard"""
        study = model.db.session.query(model.Study).get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not get this dashboard", 403
        dashboard_id = dashboard_parser.parse_args()["dashboard_id"]
        redcap_project_dashboard = model.db.session.query(
            model.StudyRedcapProjectDashboard
        ).get(dashboard_id)
        redcap_project_dashboard = redcap_project_dashboard.to_dict()
        return redcap_project_dashboard, 201

    @api.doc("redcap_project_dashboard")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def put(self, study_id: int):
        """Update study REDCap project dashboard"""
        study = model.db.session.query(model.Study).get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not modify this dashboard", 403
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "project_id",
                "dashboard_name",
                "dashboard_modules",
            ],
            "properties": {
                "project_id": {"type": "string", "minLength": 1},
                "dashboard_name": {"type": "string", "minLength": 1},
                "dashboard_modules": {
                    "type": "array",
                    "items": {
                        "anyOf": [
                            {
                                "type": "object",
                                "properties": {
                                    "key": {"type": "string", "minLength": 1},
                                    "name": {"type": "string", "minLength": 1},
                                    "selected": {"type": "boolean"},
                                    "reportId": {"type": "string", "minLength": 0},
                                },
                            }
                        ]
                    },
                    "minItems": 1,
                },
            },
        }
        data: Union[Any, dict] = request.json
        try:
            validate(request.json, schema)
        except ValidationError as e:
            print(e)
            return e.message, 400
        print("moduleslength", len(data["dashboard_modules"]))

        if len(data["project_id"]) < 1:
            return (
                f"redcap project_id is required to connect a dashboard: {data['project_id']}",
                400,
            )
        if len(data["dashboard_name"]) < 1:
            return (
                f"dashboard dashboard_name is required to connect a dashboard: {data['dashboard_name']}",
                400,
            )
        if len(data["dashboard_modules"]) < 1:
            return (
                f"dashboard dashboard_modules is required to connect a dashboard: {data['dashboard_name']}",
                400,
            )
        data["dashboard_modules"] = [
            dashboard_module
            for dashboard_module in data["dashboard_modules"]
            if dashboard_module["selected"]
        ]
        update_redcap_project_dashboard = model.StudyRedcapProjectDashboard.query.get(
            data["dashboard_id"]
        )
        update_redcap_project_dashboard.update(data)
        model.db.session.commit()
        update_redcap_project_dashboard = update_redcap_project_dashboard.to_dict()
        return update_redcap_project_dashboard, 201


@api.route("/study/<study_id>/dashboard/delete")
class DeleteRedcapProjectDashboard(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def post(self, study_id: int):
        """Delete study REDCap project dashboard"""
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not delete this redcap project", 403
        data: Union[Any, dict] = request.json
        model.StudyRedcapProjectDashboard.query.filter_by(
            dashboard_id=data["dashboard_id"]
        ).delete()
        model.db.session.commit()
        return 204
