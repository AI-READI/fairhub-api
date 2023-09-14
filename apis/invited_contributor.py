from flask_restx import Namespace, Resource, fields
from flask import request
from model import StudyInvitedContributor, Study, db, User

api = Namespace("contributor", description="contributors", path="/")


contributors_model = api.model(
    "Version",
    {
        "user_id": fields.String(required=True),
        "permission": fields.String(required=True),
        "study_id": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/invited_contributor")
class AddParticipant(Resource):
    @api.doc("invited contributor")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(contributors_model)
    def post(self, study_id: int, study, email_address: str, permission: str):
        study_obj = Study.query.get(study_id)
        user = User.query.get(email_address=email_address)
        # User exists
        if user:
            add_user_to_study(study, user, permission)
            return "Invitation is sent"
        elif not user:
            invite_user_to_study(study, user, permission)
    db.session.commit()


def add_user_to_study(study, user, permission):
    pass


def invite_user_to_study(study, user, permission):
    pass



# if study_obj.invited_contributors.email_address not in study_obj.study_contributors.user.email_address:
#     add_invited_contributor = StudyInvitedContributor.from_data(study_obj, request.json)
#     db.session.add(add_invited_contributor)