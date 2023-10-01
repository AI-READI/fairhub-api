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
        contributors = StudyContributor.query.filter_by(user_id=g.user.id, study_id=study_id).all()
        return [c.to_dict() for c in contributors]


@api.route("/study/<study_id>/contributor/<user_id>")
class ContributorResource(Resource):
    @api.doc("contributor update")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, user_id: int):
        """update contributor permissions"""
        data = request.json
        assigned_permissions = ["owner", "editor", "admin", "viewer"]
        contributors = StudyContributor.query.filter_by(
            study_id=study_id, user_id=user_id).first()
        permissions = StudyContributor.query.filter_by(
            study_id=study_id).all()
        permissions_list = [i.permission for i in permissions]
        if "owner" in permissions_list and data["permission"]== "owner":
            return "This study already contains an owner, only one owner is allowed", 403
        if data["permission"] not in assigned_permissions:
            return "Please choose one of allowed permissions", 403
        if is_granted("viewer", study_id):
            return "Access denied, viewer can not modify", 403
        if is_granted("editor", study_id):
            if data["permission"] == "owner" or data["permission"] == "admin":
                return "Access denied, editor can not modify admin or other owners", 403
        if is_granted("admin", study_id):
            if user_id != g.user.id:
                if contributors.permission == "admin" or contributors.permission == "owner":
                    return "Access denied, you can not modify other admin's or owner's permissions", 403
            elif user_id == g.user.id and data["permission"] == "owner":
                return "Access denied, you can not assign an owner", 403
        if is_granted("owner", study_id):
            if user_id != g.user.id:
                if data["permission"] == "admin":
                    return "Access denied, you can give an admin access to other contributors", 403
        contributors.update(data)
        db.session.commit()
        print(permissions_list)
        return 204

    @api.doc("contributor delete")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, user_id: int):
        contributors = StudyContributor.query.filter_by(
            study_id=study_id, user_id=user_id).first()
        if not is_granted("owner", study_id) and contributors.permission == "admin":
            return "Access denied, you can not delete admin contributors", 403
        if is_granted("editor", study_id):
            if contributors.permission == "admin" or contributors.permission == "owner":
                return "Access denied, editor can not delete admins or owners of the system", 403
        if is_granted("admin", study_id):
            if contributors.permission == "admin" or contributors.permission == "owner":
                return "Access denied, you can not delete other admin's or owner's permissions", 403
            elif user_id == g.user.id:
                return "Access denied, you can not assign an owner", 403
        db.session.delete(contributors)
        db.session.commit()
        return 204


# will need to implement it in all endpoints for which that permission is relevant
# Permissions should be only a database query and conditional statement. Failing permissions should result in a 403
