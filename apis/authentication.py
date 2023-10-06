from flask import request, make_response, g
from flask_restx import Namespace, Resource, fields
from model import StudyContributor
from datetime import timezone
import datetime
from model import db, User, TokenBlacklist, Study, StudyInvitedContributor
import jwt
import config
import uuid

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
        data = request.json
        # TODO data[email doesnt exist then raise error; json validation library
        if not data["email_address"]:
            raise "Email is not found"
        user = User.query.filter_by(email_address=data["email_address"]).one_or_none()
        if user:
            return "This email address is already in use", 409
        is_invited = StudyInvitedContributor.query.filter_by(
            email_address=data["email_address"]
        ).one_or_none()
        user_add = User.from_data(data)
        if is_invited:
            study = Study.query.filter_by(id=is_invited.study_id).first()
            contributor_add = study.add_invited_to_contributor(
                user_add, is_invited.permission
            )
            db.session.add(contributor_add)
            db.session.delete(is_invited)
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
            if len(config.secret) < 14:
                raise "secret key should contain at least 14 characters"
            encoded_jwt_code = jwt.encode(
                {
                    "user": user.id,
                    "exp": datetime.datetime.now(timezone.utc)
                    + datetime.timedelta(minutes=200),
                    "jti": str(uuid.uuid4()),
                },
                config.secret,
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
    try:
        decoded = jwt.decode(token, config.secret, algorithms=["HS256"])
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


def is_granted(permission: str, study=None):
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
    study_obj = Study.query.get(study_id)
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
        resp.status = 204
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