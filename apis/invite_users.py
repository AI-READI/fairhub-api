import os
from typing import Any, Union

from flask import g, request
from flask_restx import Namespace, Resource

import model
from invitation.invitation import send_invitation_general

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
        if os.environ.get("FLASK_ENV") != "testing":
            send_invitation_general(invited_user.email_address, invited_user.token)

        return invited_user.to_dict(), 201
