from flask import request, g
from flask_restx import Namespace, Resource, fields

from model import Study, db, User, StudyContributor
from .authentication import is_granted

api = Namespace("User", description="User tables", path="/")


study_model = api.model(
    "User",
    {

    },
)


@api.route("/profile")
class User(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_model)
    def get(self):
        """this code returns user details"""
        return User.query.all()
