from flask_restx import Namespace, Resource, fields
from model import StudyInvitedContributor, Study, db, User, StudyContributor, StudyException
from flask import request
api = Namespace("invited_contributors", description="invited contributors", path="/")


contributors_model = api.model(
    "InvitedContributor",
    {
        "user_id": fields.String(required=True),
        "permission": fields.String(required=True),
        "study_id": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/invited-contributor")
class AddInvitedContributor(Resource):
    @api.doc("invited contributor")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(contributors_model)
    def post(self, study_id: int):
        # try:
        study_obj = Study.query.get(study_id)
        data = request.json
        email_address = data["email_address"]
        user = User.query.filter_by(email_address=email_address).first()
        permission = data["permission"]
        contributor_ = None
        try:
            if user:
                contributor_ = study_obj.add_user_to_study(user, permission)
            else:
                contributor_ = study_obj.invite_user_to_study(email_address, permission)
        except StudyException as ex:
            return ex.args[0], 409
        db.session.commit()
        return contributor_.to_dict(), 201

