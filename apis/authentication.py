import datetime
import re
import uuid
from datetime import timezone
from typing import Any, Union

import jwt
from flask import g, make_response, request
from flask_restx import Namespace, Resource, fields

import config
import model

api = Namespace("Authentication", description="Authentication paths", path="/")

signup_model = api.model(
    "Signup",
    {
        "email_address": fields.String(required=True, default="sample@gmail.com"),
        "password": fields.String(required=True, default=""),
    },
)

login_model = api.model(
    "Login",
    {
        "email_address": fields.String(required=True, default=""),
        "password": fields.String(required=True, default=""),
    },
)


class UnauthenticatedException(Exception):
    pass


@api.route("/auth/signup")
class SignUpUser(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(signup_model)
    @api.expect(signup_model)
    def post(self):
        """signs up the new users and saves data in DB"""
        data: Union[Any | dict] = request.json
        # TODO data[email doesnt exist then raise error; json validation library
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not data["email_address"] or not re.match(pattern, data["email_address"]):
            return "Email address is invalid", 422
        user = model.User.query.filter_by(
            email_address=data["email_address"]
        ).one_or_none()
        if user:
            return "This email address is already in use", 409
        invitations = model.StudyInvitedContributor.query.filter_by(
            email_address=data["email_address"]
        ).all()
        new_user = model.User.from_data(data)
        for invite in invitations:
            invite.study.add_user_to_study(new_user, invite.permission)
            model.db.session.delete(invite)
        model.db.session.add(new_user)
        model.db.session.commit()
        return f"Hi, {new_user.email_address}, you have successfully signed up", 201


@api.route("/auth/login")
class Login(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(login_model)
    @api.expect(login_model)
    def post(self):
        """logs in user and handles few authentication errors.
        Also, it sets token for logged user along with expiration date"""
        data: Union[Any | dict] = request.json
        email_address = data["email_address"]
        user = model.User.query.filter_by(email_address=email_address).one_or_none()
        if not user:
            return "Invalid credentials", 401
        validate_pass = user.check_password(data["password"])
        if not validate_pass:
            return "Invalid credentials", 401
        else:
            encoded_jwt_code = jwt.encode(
                {
                    "user": user.id,
                    "exp": datetime.datetime.now(timezone.utc)
                    + datetime.timedelta(minutes=180),  # noqa: W503
                    "jti": str(uuid.uuid4()),
                },  # noqa: W503
                config.secret,
                algorithm="HS256",
            )
            resp = make_response(user.to_dict())
            resp.set_cookie(
                "token", encoded_jwt_code, secure=True, httponly=True, samesite="lax"
            )
            resp.status_code = 200
            return resp


def authentication():
    """it authenticates users to a study, sets access and refresh token.
    In addition, it handles error handling of expired token and non existed users"""
    g.user = None

    if "token" not in request.cookies:
        return
    token: str = request.cookies.get("token") if request.cookies.get("token") else ""  # type: ignore
    try:
        decoded = jwt.decode(token, config.secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return
    token_blacklist = model.TokenBlacklist.query.get(decoded["jti"])
    if token_blacklist:
        return
    user = model.User.query.get(decoded["user"])
    g.user = user


def authorization():
    """it checks whether url is allowed to be reached to specific routes"""
    # white listed routes
    public_routes = [
        "/auth",
        "/docs",
        "/echo",
        "/swaggerui",
        "/swagger.json",
    ]
    print("g.user", g.user)
    for route in public_routes:
        if request.path.startswith(route):
            return
    if g.user:
        return
    raise UnauthenticatedException("Access denied", 403)


def is_granted(permission: str, study=None):
    """filters users and checks whether current permission equal to passed permission"""
    contributor = model.StudyContributor.query.filter(
        model.StudyContributor.user == g.user, model.StudyContributor.study == study
    ).first()
    if not contributor:
        return False
    role = {
        "owner": [
            "owner",
            "view",
            "permission",
            "delete_contributor",
            "invite_contributor",
            "add_study",
            "update_study",
            "delete_study",
            "add_dataset",
            "update_dataset",
            "delete_dataset",
            "publish_version",
            "participant",
            "study_metadata",
            "dataset_metadata",
            "make_owner",
        ],
        "admin": [
            "admin",
            "view",
            "permission",
            "delete_contributor",
            "invite_contributor",
            "add_study",
            "update_study",
            "add_dataset",
            "update_dataset",
            "delete_dataset",
            "publish_version",
            "participant",
            "study_metadata",
            "dataset_metadata",
        ],
        "editor": [
            "editor",
            "view",
            "add_study",
            "update_study",
            "add_dataset",
            "update_dataset",
            "delete_dataset",
            "participant",
            "study_metadata",
            "dataset_metadata",
        ],
        "viewer": ["viewer", "view"],
    }

    return permission in role[contributor.permission]


def is_study_metadata(study_id: int):
    study_obj = model.Study.query.get(study_id)
    if not is_granted("study_metadata", study_obj):
        return "Access denied, you can not delete study", 403


@api.route("/auth/logout")
class Logout(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self):
        """simply logges out user from the system"""
        resp = make_response()
        resp.set_cookie(
            "token",
            "",
            secure=True,
            httponly=True,
            samesite="lax",
            expires=datetime.datetime.now(timezone.utc),
        )
        resp.status_code = 204
        return resp


@api.route("/auth/current-users")
class CurrentUsers(Resource):
    """function is used to see all logged users in the system. For now, it is used for testing purposes"""

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self):
        if not g.user:
            return None
        return g.user.to_dict()
