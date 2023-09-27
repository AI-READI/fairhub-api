from flask_restx import Namespace, Resource, fields
from flask import request, g
from model import StudyContributor, Study, db, User
from .authentication import is_granted
api = Namespace("Contributor", description="Contributors", path="/")


contributors_model = api.model(
    "Version",
    {
        "user_id": fields.String(required=True),
        "permission": fields.String(required=True),
        "study_id": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/contributor")
class AddContributor(Resource):
    @api.doc("contributor list")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(contributors_model)
    def get(self, study_id: int):
        contributors = StudyContributor.query.all()
        return [c.to_dict() for c in contributors]


@api.route("/study/<study_id>/contributor/<user_id>")
class ContributorResource(Resource):
    @api.doc("contributor update")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, user_id):
        if not is_granted('admin', study_id):
            return "Access denied, you can not modify permissions", 403
        if is_granted('viewer', study_id):
            return "Access denied, you can not modify", 403

        data = request.json
        contributors = StudyContributor.query.filter_by(
            study_id=study_id, user_id=user_id
        )
        contributors.permission = data
        db.session.commit()
        return contributors.permission

    @api.doc("contributor delete")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, user_id: int):
        if is_granted('viewer', study_id):
            return "Access denied, you can not modify", 403
        contributor = StudyContributor.query.filter_by(user_id=g.user.id, study_id=study_id)
        db.session.delete(contributor)
        db.session.commit()
        print(contributor)
        return 204

# will need to implement it in all endpoints for which that permission is relevant
# Permissions should be only a database query and conditional statement. Failing permissions should result in a 403
