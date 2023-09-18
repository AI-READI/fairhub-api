from flask import request
from flask_restx import Namespace, Resource, fields

from model import db, User

api = Namespace("signup", description="signup user", path="/")

signup_model = api.model(
    "Signup",
    {
        "id": fields.String(required=True),
        "email_address": fields.String(required=True),
        "username": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "orcid": fields.String(required=True),
        "hash": fields.String(required=True),
        "created_at": fields.Integer(required=True),
        "institution": fields.String(required=True),
    },
)


@api.route("/auth/signup")
class SignupUser(Resource):
    @api.doc("signup_model ")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(signup_model)
    def get(self, study_id: int):
        pass

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(signup_model)
    def post(self):
        data = request.json
        # TODO data[email doesnt exist then raise error; json validation library
        if not data["email_address"]:
            raise "Email is not found"
        user = User.query.filter_by(email_address=data["email_address"]).one_or_none()
        if user:
            return "This email address is already in use", 409
        user = User.query.filter_by(username=data["username"]).one_or_none()
        if user:
            return "This username is already in use", 409
        user = User.from_data(data)
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201
