"""API routes for study description metadata"""
from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_description = api.model(
    "StudyDescription",
    {
        "id": fields.String(required=True),
        "brief_summary": fields.String(required=True),
        "detailed_description": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/description")
class StudyDescriptionResource(Resource):
    """Study Description Metadata"""

    @api.doc("description")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(study_description)
    def get(self, study_id: int):
        """Get study description metadata"""
        study_ = model.Study.query.get(study_id)

        study_description_ = study_.study_description

        return study_description_.to_dict(), 200

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int):
        """Update study description metadata"""
        study_obj = model.Study.query.get(study_id)
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "brief_summary": {"type": "string", "minLength": 1},
                "detailed_description": {
                    "type": "string",
                },
            },
            "required": ["brief_summary", "detailed_description"],
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not modify study", 403
        study_ = model.Study.query.get(study_id)

        study_.study_description.update(request.json)

        model.db.session.commit()

        return study_.study_description.to_dict(), 200
