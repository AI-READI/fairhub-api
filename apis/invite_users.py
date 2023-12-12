from typing import Any, Union

from flask import request, g
from flask_restx import Namespace, Resource

from invitation.invitation import send_invitation_general
import model

api = Namespace("invite_general_users", description="Invite users to fairhub", path="/")


@api.route("/invite-user")
class InviteGeneralUsers(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(contributors_model)
    def post(self):
        # study_obj = model.Study.query.get(study_id)
        data: Union[dict, Any] = request.json

        email_address = data["email_address"]
        # invited_user = None
        invited_contributor = model.Invite.query.filter(
            model.Invite.email_address == email_address
        ).one_or_none()
        if invited_contributor:
            raise model.StudyException(
                "This email address has already been invited to this study"
            )
        invited_user = model.Invite(None, g.user, email_address, None)
        model.db.session.add(invited_user)
        model.db.session.commit()
        send_invitation_general(invited_user.email_address, invited_user.token)

        return invited_user.to_dict(), 201
