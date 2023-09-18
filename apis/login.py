from flask import Response, jsonify, request
from flask_restx import Namespace, Resource, fields
from model import User
from flask import redirect, url_for

api = Namespace("login", description="login", path="/")

login_model = api.model(
    "Login",
    {
        "id": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "created_at": fields.String(required=True),
        "updated_on": fields.String(required=True),
        "address": fields.String(required=True),
        "age": fields.String(required=True),
    },
)


@api.route("/auth/login")
class Login(Resource):
    @api.doc("login")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(login_model)
    def get(self, study_id: int):
        pass

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(login_model)
    def post(self):
        data = request.json
        username = data["username"]
        user = User.query.filter_by(username=username).one_or_none()
        validate_pass = user.check_password(data["password"])
        if user and validate_pass:
            return redirect(url_for("study"))
        else:
            return "Username or password is not correct", 403
