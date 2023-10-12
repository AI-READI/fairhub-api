"""API routes for study intervention metadata"""
from flask_restx import Resource, fields
from flask import request
from jsonschema import validate, ValidationError
from model import Study, db, StudyIntervention
from ..authentication import is_granted


from apis.study_metadata_namespace import api


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
        study_ = Study.query.get(study_id)

        study_intervention_ = study_.study_intervention

        sorted_study_intervention = sorted(
            study_intervention_, key=lambda x: x.created_at
        )

        return [s.to_dict() for s in sorted_study_intervention]

    def post(self, study_id: int):
        """Create study intervention metadata"""
        # Schema validation
        schema = {
            "type": "array",
            "additionalProperties": False,
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "arm_group_label_list": {"type": "array", "items": {"type": "string"}},
                    "other_name_list": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["type", "name", "description", "arm_group_label_list", "other_name_list"],
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return {"message": e.message}, 400

        study_obj = Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        list_of_elements = []
        data = request.json
        for i in data:
            if "id" in i and i["id"]:
                study_intervention_ = StudyIntervention.query.get(i["id"])
                study_intervention_.update(i)
                list_of_elements.append(study_intervention_.to_dict())
            elif "id" not in i or not i["id"]:
                study_intervention_ = StudyIntervention.from_data(study_obj, i)
                db.session.add(study_intervention_)
                list_of_elements.append(study_intervention_.to_dict())

        db.session.commit()

        return list_of_elements

    @api.route("/study/<study_id>/metadata/intervention/<intervention_id>")
    class StudyInterventionUpdate(Resource):
        """Study Intervention Metadata"""

        def delete(self, study_id: int, intervention_id: int):
            """Delete study intervention metadata"""
            study_obj = Study.query.get(study_id)
            if not is_granted("study_metadata", study_obj):
                return "Access denied, you can not delete study", 403
            study_intervention_ = StudyIntervention.query.get(intervention_id)

            db.session.delete(study_intervention_)

            db.session.commit()

            return 204
