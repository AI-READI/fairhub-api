"""API routes for study other metadata"""
from flask_restx import Resource, fields
from flask import request
from model import Study, db
from ..authentication import is_granted
from jsonschema import validate, ValidationError

from apis.study_metadata_namespace import api


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


@api.route("/study/<study_id>/metadata/other")
class StudyOtherResource(Resource):
    """Study Other Metadata"""

    @api.doc("other")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_other)
    def get(self, study_id: int):
        """Get study other metadata"""
        study_ = Study.query.get(study_id)

        study_other_ = study_.study_other

        return study_other_.to_dict()

    def put(self, study_id: int):
        """Update study other metadata"""
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "oversight_has_dmc": {"type": "boolean"},
                "conditions": {"type": "array", "items": {"type": "string"}},
                "keywords": {"type": "array", "items": {"type": "string"}},
                "size": {"type": "integer"},
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        study_ = Study.query.get(study_id)

        study_.study_other.update(request.json)

        db.session.commit()

        return study_.study_other.to_dict()


@api.route("/study/<study_id>/metadata/oversight")
class StudyOversightResource(Resource):
    """Study Oversight Metadata"""

    @api.doc("oversight")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_other)
    def get(self, study_id: int):
        """Get study oversight metadata"""
        study_ = Study.query.get(study_id)

        study_oversight_has_dmc = study_.study_other.oversight_has_dmc

        return study_oversight_has_dmc

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

        study_obj = Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        data = request.json
        study_oversight = study_obj.study_other.oversight_has_dmc = data[
            "oversight_has_dmc"
        ]
        study_obj.touch()
        db.session.commit()

        return study_oversight


# todo: rename class
@api.route("/study/<study_id>/metadata/conditions")
class StudyOversightResource(Resource):
    """Study Conditions Metadata"""

    @api.doc("conditions")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_other)
    def get(self, study_id: int):
        """Get study conditions metadata"""
        study_ = Study.query.get(study_id)

        study_other_conditions = study_.study_other.conditions

        return study_other_conditions

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

        data = request.json
        study_obj = Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        study_obj.study_other.conditions = data
        study_obj.touch()
        db.session.commit()

        return study_obj.study_other.conditions
