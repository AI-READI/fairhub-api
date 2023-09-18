from flask import Response, jsonify, request
from flask_restx import Namespace, Resource, fields

from model import Participant, Study, db, User

api = Namespace("participant", description="participant operations", path="/")

signup_model = api.model(
    "Signup",
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


@api.route("/signup")
class SignupUser(Resource):
    @api.doc("signup_model ")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(signup_model )
    def get(self, study_id: int):
        pass

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(signup_model)
    def post(self):
        data = request.json
        # TODO data[email doesnt exist then raise error; json validation library
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
