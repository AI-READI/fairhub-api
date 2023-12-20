"""API routes for study intervention metadata"""
import typing

from flask import Response, request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_intervention = api.model(
    "StudyIntervention",
    {
        "id": fields.String(required=True),
        "type": fields.String(required=True),
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "arm_group_label_list": fields.List(fields.String, required=True),
        "other_name_list": fields.List(fields.String, required=True),
    },
)


@api.route("/study/<study_id>/metadata/intervention")
class StudyInterventionResource(Resource):
    """Study Intervention Metadata"""

    @api.doc("intervention")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_intervention)
    def get(self, study_id: int):
        """Get study intervention metadata"""
        study_ = model.Study.query.get(study_id)

        study_intervention_ = study_.study_intervention

        sorted_study_intervention = sorted(
            study_intervention_, key=lambda x: x.created_at
        )

        return [s.to_dict() for s in sorted_study_intervention], 200

    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int):
        """Create study intervention metadata"""
        # Schema validation
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "type": {
                        "type": "string",
                        "enum": [
                            "Drug",
                            "Device",
                            "Biological/Vaccine",
                            "Procedure/Surgery",
                            "Radiation",
                            "Behavioral",
                            "Behavioral",
                            "Genetic",
                            "Dietary Supplement",
                            "Combination Product",
                            "Diagnostic Test",
                            "Other",
                        ],
                    },
                    "name": {"type": "string", "minLength": 1},
                    "description": {"type": "string"},
                    "arm_group_label_list": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                        "minItems": 1,
                        "uniqueItems": True,
                    },
                    "other_name_list": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                        "uniqueItems": True,
                    },
                },
                "required": ["name", "type", "arm_group_label_list"],
            },
            "uniqueItems": True,
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return {"message": e.message}, 400

        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not modify study", 403
        list_of_elements = []
        data: typing.Union[dict, typing.Any] = request.json
        for i in data:
            if "id" in i and i["id"]:
                study_intervention_ = model.StudyIntervention.query.get(i["id"])
                study_intervention_.update(i)
            else:
                study_intervention_ = model.StudyIntervention.from_data(study_obj, i)
                model.db.session.add(study_intervention_)
            list_of_elements.append(study_intervention_.to_dict())
        model.db.session.commit()

        return list_of_elements, 201

    @api.route("/study/<study_id>/metadata/intervention/<intervention_id>")
    class StudyInterventionUpdate(Resource):
        """Study Intervention Metadata"""

        @api.doc("Delete Study Interventions")
        @api.response(204, "Success")
        @api.response(400, "Validation Error")
        def delete(self, study_id: int, intervention_id: int):
            """Delete study intervention metadata"""
            study_obj = model.Study.query.get(study_id)
            if not is_granted("study_metadata", study_obj):
                return "Access denied, you can not delete study", 403
            study_intervention_ = model.StudyIntervention.query.get(intervention_id)

            model.db.session.delete(study_intervention_)

            model.db.session.commit()

            return Response(status=204)
