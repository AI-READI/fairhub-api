from flask_restx import Namespace, Resource, fields
from model import (
    Study,
    db,
    User,
    StudyException,
)
from flask import request
from .authentication import is_granted

api = Namespace("Invited_contributors", description="Invited contributors", path="/")


contributors_model = api.model(
    "InvitedContributor",
    {
        "permission": fields.String(required=True),
        "email_address": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/invited-contributor")
class AddInvitedContributor(Resource):
    @api.doc("invited contributor")
    @api.expect(contributors_model)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(contributors_model)
    def post(self, study_id: int):
        study_obj = Study.query.get(study_id)
        if not is_granted("invite_contributor", study_obj):
            return "Access denied, you can not modify", 403
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
