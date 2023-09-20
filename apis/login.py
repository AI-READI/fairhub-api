from flask import Response, jsonify, request, make_response
from flask_restx import Namespace, Resource, fields
from model import User

import jwt
import config
api = Namespace("Login", description="Login", path="/")

login_model = api.model(
    "Login",
    {
        "email_address": fields.String(required=True),
    }
)


@api.route("/auth/login")
class Login(Resource):
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
            if len(config.secret) < 14:
                raise "secret key should contain at least 14 characters"
            encoded_jwt_code = jwt.encode({"user": user.id}, config.secret, algorithm="HS256")
            resp = make_response('Setting the cookie')
            resp.set_cookie('test', encoded_jwt_code)
            return f"Authentication is successful, {resp}"


