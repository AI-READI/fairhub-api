from collections import OrderedDict

from flask_restx import Namespace, Resource, fields
from flask import request, g
from model import StudyContributor, Study, db, User
from .authentication import is_granted

api = Namespace("Contributor", description="Contributors", path="/")


contributors_model = api.model(
    "Contributor",
    {
        "permission": fields.String(required=True),

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
    @api.expect(contributors_model)
    def put(self, study_id: int, user_id: int):
        """update contributor based on the assigned permissions"""

        study = Study.query.get(study_id)
        if not is_granted("permission", study):
            return "Access denied, you are not authorized to change this permission", 403

        data = request.json
        user = User.query.get(user_id)
        permission = data["permission"]
        grantee = StudyContributor.query.filter(
            StudyContributor.user == user, StudyContributor.study == study
        ).first()

        granter = StudyContributor.query.filter(
            StudyContributor.user == g.user, StudyContributor.study == study
        ).first()

        # Order should go from the least privileged to the most privileged
        grants = OrderedDict()
        grants["viewer"] = []
        grants["editor"] = ["viewer"]
        grants["admin"] = ["viewer", "editor"]
        grants["owner"] = ["editor", "viewer", "admin"]

        can_grant = permission in grants[granter.permission]
        if not can_grant:
            return f"User cannot grant {permission}", 403

        # Granter can not downgrade anyone of equal or greater permissions other than themselves
        # TODO: Owners downgrading themselves
        if user != g.user:
            grantee_level = list(grants.keys()).index(grantee.permission) # 2
            new_level = list(grants.keys()).index(permission) # 0
            granter_level = list(grants.keys()).index(granter.permission) # 2
            if granter_level <= grantee_level and new_level < grantee_level:
                return f"User cannot downgrade from {grantee.permission} to {permission}", 403
        grantee.permission = permission
        db.session.commit()
        return grantee.to_dict(), 200

    @api.doc("contributor delete")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, user_id: int):
        data = request.json
        study = Study.query.get(study_id)
        if not is_granted("delete_contributors", study):
            return "Access denied, you are not authorized to change this permission", 403
        user = User.query.get(user_id)
        grantee = StudyContributor.query.filter(
            StudyContributor.user == user, StudyContributor.study == study
        ).first()

        granter = StudyContributor.query.filter(
            StudyContributor.user == g.user, StudyContributor.study == study
        ).first()
        # Order should go from the least privileged to the most privileged
        grants = OrderedDict()
        grants["viewer"] = []
        grants["editor"] = ["viewer"]
        grants["admin"] = ["viewer", "editor"]
        grants["owner"] = ["editor", "viewer", "admin"]

        # Granter can not downgrade anyone of equal or greater permissions other than themselves
        # TODO: Owners downgrading themselves
        if user != g.user:
            grantee_level = list(grants.keys()).index(grantee.permission)  # 2
            granter_level = list(grants.keys()).index(granter.permission)  # 2
            if granter_level <= grantee_level:
                return f"You are not authorized to delete {grantee.permission}  permission", 403
        db.session.delete(grantee)
        db.session.commit()
        return 204

