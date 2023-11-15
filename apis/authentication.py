"""This module is used to authenticate users to the system and
handle few authentication errors. Also, it sets token for logged user
along with expiration date"""
import datetime
import importlib
import os
import re
import uuid
from datetime import timezone
from typing import Any, Union

import jwt
from email_validator import EmailNotValidError, validate_email
from flask import g, make_response, request
from flask_restx import Namespace, Resource, fields
from jsonschema import FormatChecker, ValidationError, validate

import model

api = Namespace("Authentication", description="Authentication paths", path="/")

signup_model = api.model(
    "Signup",
    {
        "email_address": fields.String(required=True, default="sample@gmail.com"),
        "password": fields.String(required=True, default=""),
        "code": fields.String(required=True, default=""),
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
    """Exception raised when a user is not authenticated."""
    pass


@api.route("/auth/signup")
class SignUpUser(Resource):
    """SignUpUser class is used to sign up new users to the system"""

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(signup_model)
    @api.expect(signup_model)
    def post(self):
        """signs up the new users and saves data in DB"""
        data: Union[Any, dict] = request.json
        if os.environ.get("FLASK_ENV") != "testing":
            bypassed_emails = [
                "test@fairhub.io",
                "bpatel@fairhub.io",
                "sanjay@fairhub.io",
                "aydan@fairhub.io",
            ]

            if data["email_address"] not in bypassed_emails:
                invite = model.StudyInvitedContributor.query.filter_by(
                    email_address=data["email_address"]
                ).one_or_none()
                if not invite:
                    return "You are not validated", 403
                if invite.token != data["code"]:
                    return "signup code does not match", 403

        def validate_is_valid_email(instance):
            # Turn on check_deliverability
            # for first-time validations like on account creation pages (but not
            # login pages).
            email_address = instance
            try:
                validate_email(email_address, check_deliverability=False)
                return True
            except EmailNotValidError as e:
                raise ValidationError("Invalid email address format") from e

        def validate_password(instance):
            password = instance
            # Check if password is at least 8 characters long
            if len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long")

            # Check if password contains at least one lowercase letter
            if not re.search(r"[a-z]", password):
                raise ValidationError(
                    "Password must contain at least one lowercase letter"
                )

            # Check if password contains at least one uppercase letter
            if not re.search(r"[A-Z]", password):
                raise ValidationError(
                    "Password must contain at least one uppercase letter"
                )

            # Check if password contains at least one digit
            if not re.search(r"[0-9]", password):
                raise ValidationError("Password must contain at least one digit")

            # Check if password contains at least one special character
            if not re.search(r"[~`!@#$%^&*()_+\-={[}\]|:;\"'<,>.?/]", password):
                raise ValidationError(
                    "Password must contain at least one special character"
                )

            return True

        # Schema validation
        schema = {
            "type": "object",
            "required": ["email_address", "password", "code"],
            "additionalProperties": False,
            "properties": {
                "email_address": {"type": "string", "format": "valid_email"},
                "password": {
                    "type": "string",
                    "format": "password",
                },
                "code": {"type": "string"},
            },
        }

        format_checker = FormatChecker()
        format_checker.checks("valid_email")(validate_is_valid_email)
        format_checker.checks("password")(validate_password)

        try:
            validate(instance=data, schema=schema, format_checker=format_checker)
        except ValidationError as e:
            return e.message, 400

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
    """Login class is used to login users to the system"""

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(login_model)
    @api.expect(login_model)
    def post(self):
        """logs in user and handles few authentication errors.
        Also, it sets token for logged user along with expiration date"""
        data: Union[Any, dict] = request.json

        email_address = data["email_address"]

        def validate_is_valid_email(instance):
            email_address = instance

            try:
                validate_email(email_address)
                return True
            except EmailNotValidError as e:
                raise ValidationError("Invalid email address format") from e

        # Schema validation
        schema = {
            "type": "object",
            "required": ["email_address", "password"],
            "additionalProperties": False,
            "properties": {
                "email_address": {
                    "type": "string",
                    "format": "valid email",
                    "error_message": "Invalid email address",
                },
                "password": {"type": "string", "minLength": 8},
            },
        }

        format_checker = FormatChecker()
        format_checker.checks("valid email")(validate_is_valid_email)

        try:
            validate(instance=data, schema=schema, format_checker=format_checker)
        except ValidationError as e:
            return e.message, 400

        user = model.User.query.filter_by(email_address=email_address).one_or_none()
        if not user:
            return "Invalid credentials", 401

        validate_pass = user.check_password(data["password"])

        if not validate_pass:
            return "Invalid credentials", 401

        # Determine the appropriate configuration module
        # based on the testing context
        if os.environ.get("FLASK_ENV") == "testing":
            config_module_name = "pytest_config"
        else:
            config_module_name = "config"

        config_module = importlib.import_module(config_module_name)

        if os.environ.get("FLASK_ENV") == "testing":
            # If testing, use the 'TestConfig' class for accessing 'secret'
            config = config_module.TestConfig
        else:
            # If not testing, directly use the 'config' module
            config = config_module

        encoded_jwt_code = jwt.encode(
            {
                "user": user.id,
                "exp": datetime.datetime.now(timezone.utc)
                + datetime.timedelta(minutes=180),  # noqa: W503
                "jti": str(uuid.uuid4()),
            },  # noqa: W503
            config.FAIRHUB_SECRET,
            algorithm="HS256",
        )

        resp = make_response(user.to_dict())

        resp.set_cookie(
            "token", encoded_jwt_code, secure=True, httponly=True, samesite="None"
        )
        resp.status_code = 200

        return resp


def authentication():
    """it authenticates users to a study, sets access and refresh token.
    In addition, it handles error handling of expired token and non existed users"""
    g.user = None

    if "token" not in request.cookies:
        return
    token: str = (
        request.cookies.get("token")
        if (request.cookies.get("token"))
        else ""  # type: ignore
    )

    # Determine the appropriate configuration module based on the testing context
    if os.environ.get("FLASK_ENV") == "testing":
        config_module_name = "pytest_config"
    else:
        config_module_name = "config"
    config_module = importlib.import_module(config_module_name)
    if os.environ.get("FLASK_ENV") == "testing":
        # If testing, use the 'TestConfig' class for accessing 'secret'
        config = config_module.TestConfig
    else:
        # If not testing, directly use the 'config' module
        config = config_module
    try:
        decoded = jwt.decode(token, config.FAIRHUB_SECRET, algorithms=["HS256"])
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
            "version",
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
            "version",
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
            "version",
            "dataset_metadata",
        ],
        "viewer": ["viewer", "view"],
    }

    return permission in role[contributor.permission]


@api.route("/auth/logout")
class Logout(Resource):
    """Logout class is used to log out users from the system"""

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
            samesite="None",
            expires=datetime.datetime.now(timezone.utc),
        )
        resp.status_code = 204
        return resp


# @api.route("/auth/current-users")
# class CurrentUsers(Resource):
#     """function is used to see all logged users in
#     the system. For now, it is used for testing purposes"""

#     @api.response(200, "Success")
#     @api.response(400, "Validation Error")
#     def get(self):
#         """returns all logged users in the system"""
#         if not g.user:
#             return None
#         return g.user.to_dict()
