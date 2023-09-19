from flask import Response, jsonify, request
from flask_restx import Namespace, Resource, fields
from model import User
from flask import redirect, url_for

api = Namespace("login", description="login", path="/")

login_model = api.model(
    "Login",
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


@api.route("/auth/login")
class Login(Resource):
    @api.doc("login")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(login_model)
    def get(self):
        pass

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(login_model)
    def post(self):
        data = request.json
        email_address = data["email_address"]
        user = User.query.filter_by(email_address=email_address).one_or_none()
        if not user:
            return "Email is not correct", 403
        validate_pass = user.check_password(data["password"])
        if not validate_pass:
            return "Password is not correct", 401
        else:
            return "Authentication is successful"
