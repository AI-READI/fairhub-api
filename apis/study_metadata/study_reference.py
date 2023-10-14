"""API routes for study reference metadata"""
import typing

from flask import request
from flask_restx import Resource, fields
from jsonschema import validate, ValidationError

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_reference = api.model(
    "StudyReference",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "type": fields.String(required=True),
        "title": fields.String(required=True),
        "citation": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/reference")
class StudyReferenceResource(Resource):
    """Study Reference Metadata"""

    @api.doc("reference")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_reference)
    def get(self, study_id: int):
        """Get study reference metadata"""
        study_ = model.Study.query.get(study_id)

        study_reference_ = study_.study_reference

        sorted_study_reference = sorted(study_reference_, key=lambda x: x.created_at)

        return [s.to_dict() for s in sorted_study_reference]

    def post(self, study_id: int):
        """Create study reference metadata"""
        # Schema validation
        schema = {
            "type": "array",
            "additionalProperties": False,
            "items": {
                "type": "object",
                "properties": {
                    "identifier": {"type": "string", "minLength": 1},
                    "type": {"type": "string", "enum": ["Yes", "No"]},
                    "citation": {"type": "string", "minLength": 1},
                },
                "required": ["citation"],
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return {"message": e.message}, 400

        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        data: typing.Union[dict, typing.Any] = request.json
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                study_reference_ = model.StudyReference.query.get(i["id"])
                study_reference_.update(i)
                list_of_elements.append(study_reference_.to_dict())
            elif "id" not in i or not i["id"]:
                study_reference_ = model.StudyReference.from_data(study_obj, i)
                model.db.session.add(study_reference_)
                list_of_elements.append(study_reference_.to_dict())

        model.db.session.commit()

        return list_of_elements

    @api.route("/study/<study_id>/metadata/reference/<reference_id>")
    class StudyReferenceUpdate(Resource):
        """Study Reference Metadata"""

        def delete(self, study_id: int, reference_id: int):
            """Delete study reference metadata"""
            study_obj = model.Study.query.get(study_id)
            if not is_granted("study_metadata", study_obj):
                return "Access denied, you can not delete study", 403
            study_reference_ = model.StudyReference.query.get(reference_id)

            model.db.session.delete(study_reference_)

            model.db.session.commit()

            return 204
