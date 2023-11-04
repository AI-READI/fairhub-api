"""API routes for study redcap"""
from typing import Any, Union

from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from jsonschema import ValidationError, validate

import model

from .authentication import is_granted

api = Namespace("Redcap", description="Redcap operations", path="/")

redcap_project_view_model = api.model(
    "RedcapProjectAPI",
    {
        "study_id": fields.String(required=True),
        "project_title": fields.String(required=True),
        "project_id": fields.String(required=True),
        "project_api_url": fields.String(required=True),
        "project_api_active": fields.Boolean(required=True),
    },
)

redcap_project_api_model = api.model(
    "RedcapProjectAPI",
    {
        "study_id": fields.String(required=True),
        "project_title": fields.String(required=True),
        "project_id": fields.String(required=True),
        "project_api_key": fields.String(required=True),
        "project_api_url": fields.String(required=True),
        "project_api_active": fields.Boolean(required=True),
    },
)

redcap_project_dashboard_model = api.model(
    "RedcapProjectDashboard",
    {
        "project_id": fields.String(required=True),
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


@api.route("/study/<study_id>/redcap/all")
class RedcapProjectAPIs(Resource):
    @api.doc("redcap_project_apis")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model, as_list=True)
    def get(self, study_id: int):
        """List all study REDCap project API links"""
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not modify", 403
        # redcap_project_apis = model.StudyRedcapProjectApi.query.all(study)
        redcap_project_views = model.StudyRedcapProjectApi.query.filter_by(study=study)
        return [
            redcap_project_view.to_dict()
            for redcap_project_view in redcap_project_views
        ]


project_parser = reqparse.RequestParser().add_argument(
    "project_id", type=str, help="REDCap project ID (pid)"
)


@api.route("/study/<study_id>/redcap")
class RedcapProjectAPI(Resource):
    @api.doc(parser=project_parser)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model)
    def get(self, study_id: int):
        """Get study REDCap project API link"""
        study = model.db.session.query(model.Study).get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not modify", 403
        project_id = project_parser.parse_args()["project_id"]
        redcap_project_view = model.db.session.query(model.StudyRedcapProjectApi).get(
            project_id
        )

        if redcap_project_view is None:
            return {"error": "Project not found"}, 404

        return redcap_project_view.to_dict(), 201

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model)
    def put(self, study_id: int):
        """Update study REDCap project API link"""
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not modify", 403
        # Schema validation
        data: Union[Any, dict] = request.json
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "project_title",
                "project_id",
                "project_api_url",
                "project_api_active",
            ],
            "properties": {
                "project_title": {"type": "string", "minLength": 1},
                "project_id": {"type": "string", "minLength": 1, "maxLength": 12},
                "project_api_url": {"type": "string", "minLength": 1},
                "project_api_active": {"type": "boolean"},
            },
        }
        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        if len(data["project_title"]) < 1:
            return (
                f"redcap project_title is required for redcap access: {data['project_title']}",
                400,
            )
        if len(data["project_id"]) < 1:
            return (
                f"redcap project_id is required for redcap access: {data['project_id']}",
                400,
            )
        if len(data["project_api_url"]) < 1:
            return (
                f"redcap project_api_url is required for redcap access: {data['project_api_url']}",
                400,
            )
        if type(data["project_api_active"]) is not bool:
            return (
                f"redcap project_api_active is required for redcap access: {data['project_api_active']}",
                400,
            )

        update_redcap_project_view = model.StudyRedcapProjectApi.query.get(
            data["project_id"]
        )
        update_redcap_project_view.update(data)
        model.db.session.commit()
        return update_redcap_project_view, 201


@api.route("/study/<study_id>/redcap/add")
class AddRedcapProjectAPI(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model)
    def post(self, study_id: int):
        """Create new study REDCap project API link"""
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not modify", 403
        # Schema validation
        data: Union[Any, dict] = request.json
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "project_title",
                "project_id",
                "project_api_url",
                "project_api_key",
                "project_api_active",
            ],
            "properties": {
                "project_title": {"type": "string", "minLength": 1},
                "project_id": {"type": "string", "minLength": 5},
                "project_api_url": {"type": "string", "minLength": 1},
                "project_api_key": {"type": "string", "minLength": 32},
                "project_api_active": {"type": "boolean"},
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        if len(data["project_title"]) < 1:
            return (
                f"redcap project_title is required for redcap access: {data['project_title']}",
                400,
            )
        if len(data["project_id"]) < 1:
            return (
                f"redcap project_id is required for redcap access: {data['project_id']}",
                400,
            )
        if len(data["project_api_url"]) < 1:
            return (
                f"redcap project_api_url is required for redcap access: {data['project_api_url']}",
                400,
            )
        if len(data["project_api_key"]) < 1:
            return (
                f"redcap project_api_key is required for redcap access: {data['project_api_key']}",
                400,
            )
        if type(data["project_api_active"]) is not bool:
            return (
                f"redcap project_api_active is required for redcap access: {data['project_api_active']}",
                400,
            )

        add_redcap_project_api = model.StudyRedcapProjectApi.from_data(study, data)
        model.db.session.add(add_redcap_project_api)
        model.db.session.commit()
        return add_redcap_project_api, 201


@api.route("/study/<study_id>/redcap/delete")
class DeleteRedcapProjectAPI(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model)
    def post(self, study_id: int):
        """Delete study REDCap project API link"""
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not delete study", 403
        data: Union[Any, dict] = request.json
        delete_redcap_project_api = model.StudyRedcapProjectApi.query.filter_by(
            project_id=data["project_id"]
        ).delete()
        model.db.session.commit()
        return delete_redcap_project_api, 204


@api.route("/study/<study_id>/redcap/dashboards")
class RedcapProjectDashboards(Resource):
    """Study Redcap Metadata"""

    @api.doc("redcap_project_dashboards")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model, as_list=True)
    def get(self, study_id: int):
        """Get study redcap"""
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not modify", 403
        # redcap_project_dashboards = model.StudyRedcapProjectDashboard.query.all(study)
        redcap_project_dashboards = model.StudyRedcapProjectDashboard.query.filter_by(
            study=study
        )
        return [
            redcap_project_dashboard.to_dict()
            for redcap_project_dashboard in redcap_project_dashboards
        ]


@api.route("/study/<study_id>/redcap/dashboard")
class RedcapProjectDashboard(Resource):
    """Study Redcap Metadata"""

    @api.doc("redcap_project_dashboard")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def get(self, study_id: int, project_id: str, dashboard_id: str):
        """Get study redcap"""
        study = model.Study.query.get(study_id)
        study_redcap_project_api = model.StudyRedcapProjectApi.query.get(project_id)
        study_redcap_project_dashboard = model.StudyRedcapProjectDashboard.query.get(
            dashboard_id
        )
        if is_granted("redcap_access", study):
            return "Access denied, you can not modify", 403
        redcap_project_dashboards = model.StudyRedcapProjectDashboard.query.filter_by(
            study=study,
            study_redcap_project_api=study_redcap_project_api,
            study_redcap_project_dashboard=study_redcap_project_dashboard,
        )
        return [
            redcap_project_dashboard.to_dict()
            for redcap_project_dashboard in redcap_project_dashboards
        ]

    @api.doc("redcap_project_dashboard")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def put(self, study_id: int):
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not modify", 403
        data: Union[Any, dict] = request.json
        update_redcap_project_dashboard = model.StudyRedcapProjectDashboard.query.get(
            data["project_id"]
        )
        update_redcap_project_dashboard.update(data)
        model.db.session.commit()
        return update_redcap_project_dashboard.to_dict()

    @api.doc("redcap_project_dashboard")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_dashboard_model)
    def delete(self, study_id: int):
        """Delete study redcap metadata"""
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not delete study", 403
        data: Union[Any, dict] = request.json
        redcap_project_dashboard = model.StudyRedcapProjectDashboard.query.get(
            data["project_id"]
        )
        model.db.session.delete(redcap_project_dashboard)
        model.db.session.commit()

        return 204
