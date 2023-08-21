from flask_restx import Namespace, Resource, fields
from model import Study

api = Namespace("available_ipd", description="study operations", path="/")


study_available = api.model(
    "StudyAvailable",
    {
        "id": fields.String(required=True),
        "label": fields.String(required=True),
        "type": fields.String(required=True),
        "description": fields.String(required=True),
        "intervention_list": fields.List(fields.String, required=True),

    },
)


@api.route("/study/<study_id>/metadata/available")
class StudyArmResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    # @api.marshal_with(study_available)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_available_ = study_.study_available_ipd
        return [s.to_dict() for s in study_available_]


