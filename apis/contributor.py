from flask_restx import Namespace, Resource, fields
from flask import request, g
from model import StudyContributor, Study, db, User
from .authentication import is_granted

api = Namespace("Contributor", description="Contributors", path="/")


contributors_model = api.model(
    "Contributor",
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
        contributors = StudyContributor.query.filter_by(study_id=study_id).all()
        return [c.to_dict() for c in contributors]


@api.route("/study/<study_id>/contributor/<user_id>")
class ContributorResource(Resource):
    @api.doc("contributor update")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, user_id: int):
        """update contributor permissions"""
        if is_granted("viewer", study_id):
            return "Access denied, you can not modify", 403

        data = request.json
        contributors = StudyContributor.query.filter_by(
            study_id=study_id, user_id=user_id
        ).first()
        if is_granted("admin", study_id) and contributors.permission == "owner":
            return "Access denied, you can not modify", 403
        if (
            is_granted("admin", study_id)
            and user_id != g.user.id
            and contributors.permission == "admin"
        ):
            return "Access denied, you can not modify other admin permissions", 403
        contributors.update(data)
        db.session.commit()
        return 204

    @api.doc("contributor delete")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, user_id: int):
        if is_granted("owner", study_id):
            return "Access denied, you can not modify", 403

        contributor = StudyContributor.query.filter_by(
            user_id=user_id, study_id=study_id
        ).first()
        db.session.delete(contributor)
        db.session.commit()
        return 204


# will need to implement it in all endpoints for which that permission is relevant
# Permissions should be only a database query and conditional statement. Failing permissions should result in a 403
