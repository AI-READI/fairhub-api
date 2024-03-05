"""API routes for study other metadata"""

import typing

from flask import request, Response
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_other = api.model(
    "StudyConditions",
    {
        "id": fields.String(required=True),
        "name": fields.Boolean(required=True),
        "classification_code": fields.String(required=True),
        "scheme": fields.String(required=True),
        "scheme_uri": fields.String(required=True),
        "condition_uri": fields.String(required=True),
    },
)


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

        study_conditions = study_.study_conditions

        return [s.to_dict() for s in study_conditions], 200

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int):
        """Create study condition metadata"""
        # Schema validation
        schema = {
            "type": "array",
            "additionalProperties": False,
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string", "minLength": 1},
                    "classification_code": {"type": "string", "minLength": 1},
                    "scheme": {"type": "string"},
                    "scheme_uri": {"type": "string"},
                    "condition_uri": {"type": "string"},
                },
                "required": ["name", "classification_code", "condition_uri"],
            },
        }
        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400
        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not modify study", 403

        data: typing.Union[dict, typing.Any] = request.json
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                study_conditions_ = model.StudyConditions.query.get(i["id"])
                if not study_conditions_:
                    return f"Study condition {i['id']} Id is not found", 404
                study_conditions_.update(i)
                list_of_elements.append(study_conditions_.to_dict())
            elif "id" not in i or not i["id"]:
                study_conditions_ = model.StudyConditions.from_data(study_obj, i)
                model.db.session.add(study_conditions_)
                list_of_elements.append(study_conditions_.to_dict())
        model.db.session.commit()
        return list_of_elements, 201


@api.route("/study/<study_id>/metadata/conditions/<condition_id>")
class StudyConditionsUpdate(Resource):
    """Study Conditions Metadata update"""

    @api.doc("Delete Study Identifications")
    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, condition_id: int):
        """Delete study conditions metadata"""
        study = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study):
            return "Access denied, you can not delete study", 403

        study_conditions_ = model.StudyConditions.query.get(condition_id)

        model.db.session.delete(study_conditions_)
        model.db.session.commit()

        return Response(status=204)
