from flask_restx import Namespace, Resource, fields

from model import User

api = Namespace("contributor", description="contributors", path="/")

# contributor = api.model(
#     "Contributor",
#     {
#         "id": fields.String(required=True),
#         "firstname": fields.String(required=True),
#         "affiliations": fields.List(fields.String, required=True),
#         "email": fields.String(required=True),
#         "first_name": fields.String(required=True),
#         "last_name": fields.String(required=True),
#         "orcid": fields.String(required=True),
#         "roles": fields.List(fields.String, required=True),
#         "status": fields.String(required=True),
#         "permission": fields.String(required=True),
#     },
# )


@api.route("/study/<study_id>/contributor")
class AddParticipant(Resource):
    @api.doc("contributor list")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.param("id", "The contributor identifier")
    # @api.marshal_with(contributor)
    def get(self, study_id: int):
        contributors = User.query.all()
        return [c.to_dict() for c in contributors]
