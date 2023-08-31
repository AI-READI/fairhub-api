from flask_restx import Namespace, Resource, fields

from model import StudyContributor

api = Namespace("contributor", description="contributors", path="/")


contributors_model = api.model(
    "Version",
    {
        "user_id": fields.String(required=True),
        "permission": fields.String(required=True),
        "study_id": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/contributor")
class AddParticipant(Resource):
    @api.doc("contributor list")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(contributors_model)
    def get(self, study_id: int):
        contributors = StudyContributor.query.all()
        return [c.to_dict() for c in contributors]

    def post(self, study_id: int):
        contributors = StudyContributor.query.all()
