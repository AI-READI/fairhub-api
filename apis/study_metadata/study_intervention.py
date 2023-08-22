from model import Study

from flask_restx import Namespace, Resource, fields


api = Namespace("intervention", description="study operations", path="/")


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
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_intervention)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_intervention_ = study_.study_intervention
        return [s.to_dict() for s in study_intervention_]
