from flask import Response, jsonify, request
from flask_restx import Namespace, Resource, fields

from model import Participant, Study, db

api = Namespace("participant", description="participant operations", path="/")

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


@api.route("/login")
class Login(Resource):
    @api.doc("participants")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(login_model)
    def get(self, study_id: int):
        pass

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(login_model)

    def post(self, study_id: int):
        # user query using username
        # call user check password

        pass


