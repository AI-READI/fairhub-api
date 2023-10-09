from flask import request, g
from flask_restx import Namespace, Resource, fields

from model import Study, db, User, StudyContributor
from .authentication import is_granted

api = Namespace("User", description="User tables", path="/")


study_model = api.model(
    "User",
    {
        "first_name": fields.String(required=True, default=""),
        "last_name": fields.String(required=True, default=""),
        "institution": fields.String(required=True, default=""),
        "orcid": fields.String(required=True, default=""),
        "location": fields.String(required=True, default=""),
        "timezone": fields.String(required=True, default=""),
    },
)


@api.route("/profile")
class UserDetails(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_model)
    def get(self):
        """This code returns user details"""
        user = User.query.get(g.user.id)
        return user.to_dict()
    
    @api.expect(study_model)
    def put(self):
        """This code updates user details"""
        data = request.json
        user = User.query.get(g.user.id)
        user.update(data)
        db.session.commit()
        return user.to_dict()