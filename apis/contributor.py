from collections import OrderedDict

from flask_restx import Namespace, Resource, fields
from flask import request, g
from model import (
    Study,
    db,
    User,
    StudyException,
    StudyContributor,
    StudyInvitedContributor
)
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
        # study_contributors = (
        #     StudyContributor.query
        #     .filter(StudyContributor.user_id == g.user.id)  # Filter contributors where user_id matches the user's id
        #     .all()
        # )
        contributors = StudyContributor.query.filter_by(
             study_id=study_id
        ).all()
        invited_contributors = StudyInvitedContributor.query.filter_by(
             study_id=study_id
        ).all()

        contributors_list = [c.to_dict() for c in contributors] + [c.to_dict() for c in invited_contributors]
        return contributors_list


    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(contributors_model)
    def post(self, study_id: int):
        study_obj = Study.query.get(study_id)
        if not is_granted("invite_contributor", study_obj):
            return "Access denied, you can not modify", 403
        data = request.json
        email_address = data["email_address"]
        user = User.query.filter_by(email_address=email_address).first()
        permission = data["role"]
        contributor_ = None
        try:
            if user:
                contributor_ = study_obj.add_user_to_study(user, permission)
            else:
                contributor_ = study_obj.invite_user_to_study(email_address, permission)
        except StudyException as ex:
            return ex.args[0], 409
        db.session.commit()
        return contributor_.to_dict(), 201


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
            return (
                "Access denied, you are not authorized to change this permission",
                403,
            )
        data = request.json
        user = User.query.get(user_id)
        permission = data["role"]
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
        grants["admin"] = ["viewer", "editor", "admin"]
        grants["owner"] = ["editor", "viewer", "admin"]

        can_grant = permission in grants[granter.permission]
        if not can_grant:
            return f"User cannot grant {permission}", 403

        # Granter can not downgrade anyone of equal or greater permissions other than themselves
        # TODO: Owners downgrading themselves
        if user != g.user:
            grantee_level = list(grants.keys()).index(grantee.permission)  # 1
            new_level = list(grants.keys()).index(permission)  #  2
            granter_level = list(grants.keys()).index(granter.permission)  # 2
            if granter_level <= grantee_level and new_level <= grantee_level:
                return (
                    f"User cannot downgrade from {grantee.permission} to {permission}",
                    403,
                )
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
            return (
                "Access denied, you are not authorized to change this permission",
                403,
            )
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
                return (
                    f"You are not authorized to delete {grantee.permission}s from study",
                    403,
                )
        db.session.delete(grantee)
        db.session.commit()
        contributors = StudyContributor.query.filter(
            StudyContributor.study == study
        ).all()
        return [contributor.to_dict() for contributor in contributors], 200


@api.route("/study/<study_id>/owner/<user_id>")
class AssignOwner(Resource):
    @api.doc("contributor update")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.expect(contributors_model)
    def put(self, study_id: int, user_id: int):
        data = request.json
        """set owner based on the assigned permissions"""
        study = Study.query.get(study_id)
        if not is_granted("make_owner", study):
            return "Access denied, you are not authorized to change this permission", 403
        if not data["role"] == "owner":
            return "you can assign only owner", 403
        user = User.query.get(user_id)
        existing_contributor = StudyContributor.query.filter(
            StudyContributor.user == user,
            StudyContributor.study == study,

        ).first()
        existing_contributor.permission = "owner"
        existing_owner = StudyContributor.query.filter(
            StudyContributor.study == study,
            StudyContributor.permission == "owner"
        ).first()
        existing_owner.permission = "admin"
        db.session.commit()
        return existing_contributor.to_dict(), 200
