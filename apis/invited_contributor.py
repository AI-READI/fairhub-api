from flask_restx import Namespace, Resource, fields

from model import StudyInvitedContributor, Study

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
    @api.doc("invited contributor")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(contributors_model)
    def post(self, study_id: int, invited_contributor_id: int):
        invited_contributors = Study.query.get(invited_contributor_id)

