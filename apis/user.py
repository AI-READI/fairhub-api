from flask import request, g
from flask_restx import Namespace, Resource, fields

from model import User, db

api = Namespace("User", description="User tables", path="/")


study_model = api.model(
    "User",
    {
        "email_address": fields.String(required=True, default=""),
        "username": fields.String(required=True, default=""),
        "first_name": fields.String(required=True, default=""),
        "last_name": fields.String(required=True, default=""),
        "institution": fields.String(required=True, default=""),
        "orcid": fields.String(required=True, default=""),
        "location": fields.String(required=True, default=""),
        "timezone": fields.String(required=True, default=""),
        "profile_image": fields.String(required=False, default=""),
    },
)


@api.route("/user/profile")
class UserDetailsEndpoint(Resource):
    @api.doc("list_study")
    @api.response(200, "Success", study_model)
    @api.response(400, "Validation Error")
    def get(self):
        """Returns user details"""
        user = User.query.get(g.user.id)
        user_details = user.user_details
        user_information = user.to_dict()
        user_information.update(user_details.to_dict())
        return user_information

    @api.expect(study_model)
    @api.marshal_with(study_model)
    def put(self):
        """Updates user details"""
        data = request.json
        if data is None:
            return {"message": "No data provided"}, 400
        user = User.query.get(g.user.id)
        user.update(data)
        user_details = user.user_details
        user_details.update(data)
        db.session.commit()
        return user_details.to_dict()
