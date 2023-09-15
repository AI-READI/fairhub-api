from flask_restx import Namespace, Resource, fields
from model import StudyInvitedContributor, Study, db, User, StudyContributor
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
        if user:
            study_obj.add_user_to_study(user, permission)

        elif not user:
            study_obj.invite_user_to_study(email_address, permission)
            print("User successfully saved")
        db.session.commit()
        # except:
        #     print("error occured", 422)

