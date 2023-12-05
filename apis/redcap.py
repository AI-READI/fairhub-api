"""API routes for study redcap"""
from typing import Any, Union

from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from jsonschema import ValidationError, validate

import model

from .authentication import is_granted

api = Namespace("Redcap", description="REDCap operations", path="/")

redcap_project_view_model = api.model(
    "RedcapProjectAPI",
    {
        "study_id": fields.String(required=True, description="Study ID"),
        "project_id": fields.String(
            required=True, description="REDCap project ID (pid)"
        ),
        "project_title": fields.String(
            required=True, description="REDCap project title"
        ),
        "project_api_url": fields.String(
            required=True, description="REDCap project API url"
        ),
        "project_api_active": fields.Boolean(
            required=True, description="REDCap project is active"
        ),
    },
)

redcap_project_api_model = api.model(
    "RedcapProjectAPI",
    {
        "study_id": fields.String(required=True, description="Study ID"),
        "project_id": fields.String(
            required=True, description="REDCap project ID (pid)"
        ),
        "project_title": fields.String(
            required=True, description="REDCap project title"
        ),
        "project_api_key": fields.String(
            required=True, description="REDCap project API key"
        ),
        "project_api_url": fields.String(
            required=True, description="REDCap project API url"
        ),
        "project_api_active": fields.Boolean(
            required=True, description="REDCap project is active"
        ),
    },
)

project_parser = reqparse.RequestParser()
project_parser.add_argument("project_id", type=str, help="REDCap project ID (pid)")


@api.route("/study/<study_id>/redcap/all")
class RedcapProjectAPIs(Resource):
    @api.doc("redcap_project_apis")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model, as_list=True)
    def get(self, study_id: int):
        """Get all REDCap project API links"""
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return (
                "Access denied, you can not view the redcap projects for this study",
                403,
            )
        redcap_project_views = model.StudyRedcapProjectApi.query.filter_by(study=study)
        redcap_project_views = [
            redcap_project_view.to_dict()
            for redcap_project_view in redcap_project_views
        ]
        return redcap_project_views, 201


@api.route("/study/<study_id>/redcap/add")
class AddRedcapProjectAPI(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model)
    def post(self, study_id: int):
        """Create REDCap project API link"""
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not create a redcap project", 403
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
                f"redcap project_title is required for redcap access: \
                {data['project_title']}",
                400,
            )
        if len(data["project_id"]) < 1:
            return (
                f"redcap project_id is required for redcap access: \
                {data['project_id']}",
                400,
            )
        if len(data["project_api_url"]) < 1:
            return (
                f"redcap project_api_url is required for redcap access: \
                {data['project_api_url']}",
                400,
            )
        if len(data["project_api_key"]) < 1:
            return (
                f"redcap project_api_key is required for redcap access: \
                {data['project_api_key']}",
                400,
            )
        if isinstance(data["project_api_active"], bool):
            return (
                f"redcap project_api_active is required for redcap access: \
                {data['project_api_active']}",
                400,
            )

        add_redcap_project_api = model.StudyRedcapProjectApi.from_data(study, data)
        model.db.session.add(add_redcap_project_api)
        model.db.session.commit()
        add_redcap_project_api = add_redcap_project_api.to_dict()
        return add_redcap_project_api, 201


@api.route("/study/<study_id>/redcap")
class RedcapProjectAPI(Resource):
    @api.doc(parser=project_parser)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model)
    def get(self, study_id: int):
        """Get REDCap project API link"""
        study = model.db.session.query(model.Study).get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not get this redcap project", 403
        project_id = project_parser.parse_args()["project_id"]
        redcap_project_view: Any = model.db.session.query(
            model.StudyRedcapProjectApi
        ).get(project_id)
        redcap_project_view = redcap_project_view.to_dict()
        return redcap_project_view, 201


@api.route("/study/<study_id>/redcap/edit")
class EditRedcapProjectAPI(Resource):
    @api.doc(parser=project_parser)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model)
    def put(self, study_id: int):
        """Update REDCap project API link"""
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not modify this redcap project", 403
        # Schema validation
        data: Union[Any, dict] = request.json
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "project_id",
                "project_title",
                "project_api_url",
                "project_api_active",
            ],
            "properties": {
                "project_id": {"type": "string", "minLength": 1, "maxLength": 12},
                "project_title": {"type": "string", "minLength": 1},
                "project_api_url": {"type": "string", "minLength": 1},
                "project_api_active": {"type": "boolean"},
            },
        }
        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        if len(data["project_id"]) < 1:
            return (
                f"redcap project_id is required for redcap access: \
                {data['project_id']}",
                400,
            )
        if len(data["project_title"]) < 1:
            return (
                f"redcap project_title is required for redcap access: \
                {data['project_title']}",
                400,
            )
        if len(data["project_api_url"]) < 1:
            return (
                f"redcap project_api_url is required for redcap access: \
                {data['project_api_url']}",
                400,
            )
        if isinstance(data["project_api_active"], bool):
            return (
                f"redcap project_api_active is required for redcap access: \
                {data['project_api_active']}",
                400,
            )

        update_redcap_project_view = model.StudyRedcapProjectApi.query.get(
            data["project_id"]
        )
        update_redcap_project_view.update(data)
        model.db.session.commit()
        update_redcap_project_view = update_redcap_project_view.to_dict()
        return update_redcap_project_view, 201


@api.route("/study/<study_id>/redcap/delete")
class DeleteRedcapProjectAPI(Resource):
    @api.doc(parser=project_parser)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_project_view_model)
    def delete(self, study_id: int):
        """Delete REDCap project API link"""
        study = model.Study.query.get(study_id)
        if is_granted("redcap_access", study):
            return "Access denied, you can not delete this redcap project", 403
        project_id = project_parser.parse_args()["project_id"]
        model.StudyRedcapProjectApi.query.filter_by(project_id=project_id).delete()
        model.db.session.commit()
        return 204
