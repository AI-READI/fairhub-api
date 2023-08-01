from model import User
from flask_restx import Resource, Namespace, fields

api = Namespace("contributor", description="contributors", path="/")

contributor = api.model(
    "Contributor",
    {
        "id": fields.String(required=True),
        "firstname": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/contributor")
class AddParticipant(Resource):
    @api.doc("contributor list")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.param("id", "The contributor identifier")
    @api.marshal_with(contributor)
    def get(self, study_id: int):
        contributors = User.query.all()
        return [c.to_dict() for c in contributors]
