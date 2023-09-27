from flask import request, make_response, g
from flask_restx import Namespace, Resource, fields
from model import StudyContributor
from datetime import timezone
import datetime
from dateutil.parser import parse
from model import db, User
import jwt
import config

api = Namespace("Authentication", description="Authentication paths", path="/")

signup_model = api.model(
    "Signup",
    {
        "id": fields.String(required=True),
        "email_address": fields.String(required=True),
        "email_verified": fields.String(required=True),
        "username": fields.String(required=True),
        "created_at": fields.Integer(required=True),
    },
)


class AccessDenied(Exception):
    pass


@api.route("/auth/signup")
class SignUpUser(Resource):

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(signup_model)
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
        user = User.from_data(data)
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201


@api.route("/auth/login")
class Login(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(login_model)
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


def authentication():
    """it authenticates users to a study, sets access and refresh token.
    In addition, it handles error handling of expired token and non existed users"""
    g.user = None
    if "user" not in request.cookies:
        return
    # if 'user' in
    token = request.cookies.get("user")
    try:
        decoded = jwt.decode(token, config.secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        # Handle token expiration error here (e.g., re-authenticate the user)
        return "Token has expired, please re-authenticate", 401
    user = User.query.get(decoded["user"])
    g.user = user
    expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60)
    new_token = jwt.encode({"exp": expires}, config.secret, algorithm="HS256")
    resp = make_response("Token refreshed")
    resp.set_cookie("user", new_token, secure=True, httponly=True, samesite="lax")
    return resp


@api.route("/auth/logout")
class Logout(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self):
        """simply logges out user from the system"""
        resp = make_response()
        resp.status = 204
        resp.delete_cookie("user")
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


def authorization():
    """it checks whether url is allowed to be reached"""
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
