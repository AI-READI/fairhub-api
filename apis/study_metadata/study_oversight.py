"""API routes for study other metadata"""

import typing

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_other = api.model(
    "StudyOversight",
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

        study_oversight_has_dmc = study_.study_oversight
        return study_oversight_has_dmc.to_dict(), 200

    def put(self, study_id: int):
        """Update study oversight metadata"""
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {"oversight_has_dmc": {"type": "boolean"}},
            "required": ["has_dmc"],
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not modify study", 403
        data: typing.Union[dict, typing.Any] = request.json
        study_obj.study_oversight.update(data)
        model.db.session.commit()
        return study_obj.study_oversight.to_dict(), 200
