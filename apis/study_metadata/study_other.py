"""API routes for study other metadata"""
import typing

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_other = api.model(
    "StudyOther",
    {
        "id": fields.String(required=True),
        "oversight_has_dmc": fields.Boolean(required=True),
        "conditions": fields.String(required=True),
        "keywords": fields.String(required=True),
        "size": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/oversight")
class StudyOversightResource(Resource):
    """Study Oversight Metadata"""

    @api.doc("oversight")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_other)
    def get(self, study_id: int):
        """Get study oversight metadata"""
        study_ = model.Study.query.get(study_id)

        study_oversight_has_dmc = study_.study_other.oversight_has_dmc
        return {"oversight": study_oversight_has_dmc}, 200

    def put(self, study_id: int):
        """Update study oversight metadata"""
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {"oversight_has_dmc": {"type": "boolean"}},
            "required": ["oversight_has_dmc"],
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not modify study", 403
        data: typing.Union[dict, typing.Any] = request.json
        study_oversight = study_obj.study_other.oversight_has_dmc = data[
            "oversight_has_dmc"
        ]
        study_obj.touch()
        model.db.session.commit()

        return study_oversight, 200


@api.route("/study/<study_id>/metadata/conditions")
class StudyCondition(Resource):
    """Study Conditions Metadata"""

    @api.doc("conditions")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_other)
    def get(self, study_id: int):
        """Get study conditions metadata"""
        study_ = model.Study.query.get(study_id)

        study_other_conditions = study_.study_other.conditions

        return study_other_conditions, 200

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int):
        """Update study conditions metadata"""
        # Schema validation
        schema = {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
            "minItems": 1,
            "uniqueItems": True,
            "additionalItems": False,
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: typing.Union[dict, typing.Any] = request.json
        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not modify study", 403
        study_obj.study_other.conditions = data
        study_obj.touch()
        model.db.session.commit()

        return study_obj.study_other.conditions, 200


@api.route("/study/<study_id>/metadata/keywords")
class StudyKeywords(Resource):
    """Study Keywords Metadata"""

    @api.doc("keywords")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_other)
    def get(self, study_id: int):
        """Get study keywords metadata"""
        study_ = model.Study.query.get(study_id)

        study_other_keywords = study_.study_other.keywords

        return study_other_keywords, 200

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int):
        """Update study keywords metadata"""
        # Schema validation
        schema = {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
            "minItems": 1,
            "uniqueItems": True,
            "additionalItems": False,
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: typing.Union[dict, typing.Any] = request.json
        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not modify study", 403
        study_obj.study_other.keywords = data
        study_obj.touch()
        model.db.session.commit()

        return study_obj.study_other.keywords, 200
