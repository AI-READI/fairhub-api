from flask import request, make_response, g
from flask_restx import Namespace, Resource, fields
from model import StudyContributor
from datetime import timezone
import datetime
from model import db, User, TokenBlacklist
import jwt

# import config
import uuid
import os
import importlib

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


class AccessDenied(Exception):
    pass


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
        data = request.json
        # TODO data[email doesnt exist then raise error; json validation library
        if not data["email_address"]:
            raise "Email is not found"
        user = User.query.filter_by(email_address=data["email_address"]).one_or_none()
        if user:
            return "This email address is already in use", 409
        # user = User.query.filter_by(username=data["username"]).one_or_none()
        # if user:
        #     return "This username is already in use", 409
        user_add = User.from_data(data)
        # user.user_details.update(data)
        db.session.add(user_add)
        db.session.commit()
        return f"Hi, {user_add.email_address}, you have successfully signed up", 201


@api.route("/auth/login")
class Login(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(login_model)
    @api.expect(login_model)
    def post(self):
        """logs in user and handles few authentication errors.
        Also, it sets token for logged user along with expiration date"""
        data = request.json
        email_address = data["email_address"]
        user = User.query.filter_by(email_address=email_address).one_or_none()
        if not user:
            return "Invalid credentials", 401
        validate_pass = user.check_password(data["password"])
        if not validate_pass:
            return "Invalid credentials", 401
        else:
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
    
            if len(config.FAIRHUB_SECRET) < 14:
                raise "secret key should contain at least 14 characters"
            encoded_jwt_code = jwt.encode(
                {
                    "user": user.id,
                    "exp": datetime.datetime.now(timezone.utc)
                    + datetime.timedelta(minutes=20),
                    "jti": str(uuid.uuid4()),
                },
                config.FAIRHUB_SECRET,
                algorithm="HS256",
            )
            resp = make_response(user.to_dict())
            resp.set_cookie(
                "token", encoded_jwt_code, secure=True, httponly=True, samesite="lax"
            )
            resp.status = 200
            return resp


def authentication():
    """it authenticates users to a study, sets access and refresh token.
    In addition, it handles error handling of expired token and non existed users"""
    g.user = None
    if "token" not in request.cookies:
        return
    token = request.cookies.get("token")
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
    token_blacklist = TokenBlacklist.query.get(decoded["jti"])
    if token_blacklist:
        return
    user = User.query.get(decoded["user"])
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


def is_granted(permission: str, study):
    """filters users and checks whether current permission equal to passed permission"""
    contributor = StudyContributor.query.filter(
        StudyContributor.user == g.user, StudyContributor.study == study
    ).first()
    if not contributor:
        return False
    role = {
        "owner": [
            "owner",
            "view",
            "delete_study",
            "delete_contributor",
            "invite_contributor",
            "publish_dataset",
            "add_dataset",
            "delete_dataset",
            "permission",
            "edit_study",
            "update_participant" "delete_participant",
        ],
        "admin": [
            "admin",
            "view",
            "invite_contributor",
            "publish_dataset",
            "add_dataset",
            "delete_dataset",
            "permission",
            "update_participant",
            "delete_participant",
        ],
        "editor": [
            "editor",
            "view",
            "add_dataset",
            "permission",
            "update_participant",
            "delete_participant",
        ],
        "viewer": ["viewer", "view"],
    }

    return permission in role[contributor.permission]


@api.route("/auth/logout")
class Logout(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self):
        """simply logges out user from the system"""
        resp = make_response()
        resp.status = 204
        resp.delete_cookie("token")
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
