"""API routes for study redcap"""
import typing

from flask import request
from flask_restx import Namespace, Resource, fields
from jsonschema import ValidationError, validate

import model

from .authentication import is_granted

api = Namespace("Redcap", description="Redcap operations", path="/")

redcap_model = api.model(
    "Redcap",
    {
        "id": fields.String(required=True),
        "redcap_api_token": fields.String(required=True),
        "redcap_api_url": fields.String(required=True),
        "redcap_project_id": fields.String(required=True),
        "redcap_report_id_survey_completions": fields.String(required=True),
        "redcap_report_id_repeat_surveys": fields.String(required=True),
        "redcap_report_id_participant_values": fields.String(required=True),
        "redcap_report_id_participants": fields.String(required=True),
    },
)

@api.route("/study/<study_id>/redcap")
class Redcap(Resource):
    """Study Redcap Metadata"""

    @api.doc("redcap")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_model)
    def get(self, study_id: int, redcap_project_id: str):
        """Get study redcap"""
        study_ = model.Study.query.get(study_id)
        study_redcap_ = study_.study_redcap
        return study_redcap_.to_dict()

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_model)
    def post(self, study_id: int):
        """Update study redcap"""
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "redcap_api_token",
                "redcap_api_url",
                "redcap_project_id",
                "redcap_report_id_survey_completions",
                "redcap_report_id_repeat_surveys",
                "redcap_report_id_participant_values",
                "redcap_report_id_participants",
            ],
            "properties": {
                "redcap_api_token": {"type": string, "minLength": 1},
                "redcap_api_url": {"type": string, "minLength": 1},
                "redcap_project_id": {"type": string, "minLength": 1},
                "redcap_report_id_participants": {"type": string, "minLength": 1},
                "redcap_report_id_survey_completions": {"type": string},
                "redcap_report_id_repeat_surveys": {"type": string},
                "redcap_report_id_participant_values": {"type": string},
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: typing.Union[typing.Any, dict] = request.json
        if len(data["redcap_api_url"]) < 1:
            return (
                f"recap_api_url is required for redcap access: {data['redcap_api_url']}",
                400,
            )
        if len(data["redcap_api_token"]) < 1:
            return (
                f"recap_api_token is required for redcap access: {data['redcap_api_token']}",
                400,
            )
        if len(data["redcap_project_id"]) < 1:
            return (
                f"recap_project_id is required for redcap access: {data['redcap_project_id']}",
                400,
            )

        study_obj = model.Study.query.get(study_id)
        if not is_granted("viewer", study_id):
            return "Access denied, you can not modify", 403
        study = model.Study.query.get(study_id)
        study.study_redcap.update(request.json)
        model.db.session.commit()

        return study.study_redcap.to_dict()

@api.route("/study/<study_id>/redcap/<redcap_project_id>")
class RedcapUpdate(Resource):
    @api.doc("redcap")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_model)
    def delete(self, study_id: int, redcap_project_id: str):
        """Delete study redcap metadata"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        study_redcap_ = model.StudyRedcap.query.get(study_id)
        model.db.session.delete(study_redcap_)
        model.db.session.commit()

        return 204

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_model)
    def put(self, study_id: int):
        """Update study redcap"""
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "redcap_api_token",
                "redcap_api_url",
                "redcap_project_id",
                "redcap_report_id_survey_completions",
                "redcap_report_id_repeat_surveys",
                "redcap_report_id_participant_values",
                "redcap_report_id_participants",
            ],
            "properties": {
                "redcap_api_token": {"type": string, "minLength": 1},
                "redcap_api_url": {"type": string, "minLength": 1},
                "redcap_project_id": {"type": string, "minLength": 1},
                "redcap_report_id_participants": {"type": string, "minLength": 1},
                "redcap_report_id_survey_completions": {"type": string},
                "redcap_report_id_repeat_surveys": {"type": string},
                "redcap_report_id_participant_values": {"type": string},
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: typing.Union[typing.Any, dict] = request.json
        if len(data["redcap_api_url"]) < 1:
            return (
                f"recap_api_url is required for redcap access: {data['redcap_api_url']}",
                400,
            )
        if len(data["redcap_api_token"]) < 1:
            return (
                f"recap_api_token is required for redcap access: {data['redcap_api_token']}",
                400,
            )
        if len(data["redcap_project_id"]) < 1:
            return (
                f"recap_project_id is required for redcap access: {data['redcap_project_id']}",
                400,
            )

        study_obj = model.Study.query.get(study_id)
        if not is_granted("viewer", study_id):
            return "Access denied, you can not modify", 403
        study = model.Study.query.get(study_id)
        study.study_redcap.update(request.json)
        model.db.session.commit()

        return study.study_redcap.to_dict()

