from flask import jsonify, request, make_response, g
from flask_restx import Namespace, Resource, fields
from model import User, StudyContributor
import uuid
from datetime import timezone
import datetime
from dateutil.parser import parse

import jwt
import config

api = Namespace("Login", description="Login", path="/")


class AccessDenied(Exception):
    pass


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
            return "Invalid credentials", 401
        validate_pass = user.check_password(data["password"])
        if not validate_pass:
            return "Invalid credentials", 401
        else:
            if len(config.secret) < 14:
                raise "secret key should contain at least 14 characters"
            encoded_jwt_code = jwt.encode(
                {
                    "user": user.id,
                    "exp": datetime.datetime.now(timezone.utc)
                    + datetime.timedelta(minutes=60),
                },
                config.secret,
                algorithm="HS256",
            )
            resp = make_response(user.to_dict())
            resp.set_cookie(
                "user", encoded_jwt_code, secure=True, httponly=True, samesite="lax"
            )
            resp.status = 200
            return resp


@api.route("/auth/logout")
class Logout(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self):
        resp = make_response()
        resp.status = 204
        resp.delete_cookie("user")
        return resp


@api.route("/auth/current-users")
class CurrentUsers(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self):
        if not g.user:
            return None
        return g.user.to_dict()


def authentication():
    g.user = None
    if "user" not in request.cookies:
        return
    # if 'user' in
    token = request.cookies.get("user")
    try:
        decoded = jwt.decode(token, config.secret, algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return
    user = User.query.get(decoded["user"])
    g.user = user
    decoded = jwt.decode(token, config.secret, algorithms=["HS256"])


def authorization():
    """check whether url is allowed to be reached"""
    # white listed routes
    public_routes = [
        "/auth",
        "/docs",
        "/echo",
        "/swaggerui",
        "/swagger.json",
    ]
    for route in public_routes:
        if request.path.startswith(route):
            return
    if g.user:
        return
    raise AccessDenied("Access denied")


def is_granted(permission: str, study_id: int):
    """filters users and checks whether current permission equal to passed permission"""
    contributor = StudyContributor.query.filter_by(
        user_id=g.user.id, study_id=study_id
    ).first()
    return contributor.permission == permission
