from collections import OrderedDict
from typing import Any, Dict, List, Union

from flask import g, request, Response
from flask_restx import Namespace, Resource, fields

import model

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
        contributors = model.StudyContributor.query.filter_by(study_id=study_id).all()
        invited_contributors = model.StudyInvitedContributor.query.filter_by(
            study_id=study_id
        ).all()

        contributors_list = [c.to_dict() for c in contributors] + [
            c.to_dict() for c in invited_contributors
        ]
        return contributors_list

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(contributors_model)
    def post(self, study_id: int):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("invite_contributor", study_obj):
            return "Access denied, you can not modify study", 403
        data: Union[dict, Any] = request.json

        email_address = data["email_address"]
        user = model.User.query.filter_by(email_address=email_address).first()
        permission = data["role"]
        contributor_ = None

        try:
            if user:
                contributor_ = study_obj.add_user_to_study(user, permission)
            else:
                contributor_ = study_obj.invite_user_to_study(email_address, permission)

        except model.StudyException as ex:
            return ex.args[0], 409
        model.db.session.commit()
        return contributor_.to_dict(), 201


@api.route("/study/<study_id>/contributor/<user_id>")
class ContributorResource(Resource):
    @api.doc("contributor update")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.expect(contributors_model)
    def put(self, study_id: int, user_id: int):
        """update contributor based on the assigned permissions"""
        study = model.Study.query.get(study_id)
        if not study:
            return "study is not found", 404
        if not is_granted("permission", study):
            return (
                "Access denied, you are not authorized to change this permission",
                403,
            )
        data: Union[Any, dict] = request.json
        user = model.User.query.get(user_id)
        if not user:
            return "user not found", 404
        permission: Union[Any, str] = data["role"]
        grantee = model.StudyContributor.query.filter(
            model.StudyContributor.user == user, model.StudyContributor.study == study
        ).first()
        granter = model.StudyContributor.query.filter(
            model.StudyContributor.user == g.user, model.StudyContributor.study == study
        ).first()
        # Order should go from the least privileged to the most privileged
        grants: Dict[str, List[str]] = OrderedDict()
        grants["viewer"] = []
        grants["editor"] = ["viewer"]
        grants["admin"] = ["viewer", "editor", "admin"]
        grants["owner"] = ["editor", "viewer", "admin"]

        can_grant = permission in grants[granter.permission]
        if not can_grant:
            return f"User cannot grant {permission}", 403

        # TODO: Owners downgrading themselves
        if user != g.user:
            grantee_level = list(grants.keys()).index(grantee.permission)  # 1
            new_level: int = list(grants.keys()).index(str(permission))  # 2
            granter_level = list(grants.keys()).index(granter.permission)  # 2
            if granter_level <= grantee_level and new_level <= grantee_level:
                return (
                    f"User cannot downgrade from {grantee.permission} to {permission}",
                    403,
                )
        grantee.permission = permission
        model.db.session.commit()
        return grantee.to_dict(), 200

    @api.doc("contributor delete")
    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, user_id: str):
        study = model.Study.query.get(study_id)
        if not study:
            return "study is not found", 404
        granter = model.StudyContributor.query.filter(
            model.StudyContributor.user == g.user, model.StudyContributor.study == study
        ).first()
        if not granter:
            return "you are not contributor of this study", 403
        grants: Dict[str, List[str]] = OrderedDict()
        grants["viewer"] = []
        grants["editor"] = []
        grants["admin"] = ["viewer", "editor"]
        grants["owner"] = ["editor", "viewer", "admin"]

        if "@" in user_id:
            invited_grantee = model.StudyInvitedContributor.query.filter_by(
                study_id=study_id, email_address=user_id
            ).first()
            # invited_grants: Union[OrderedDict
            # [str, List[str]]] = OrderedDict()
            invited_grants: Dict[str, List[str]] = OrderedDict()
            invited_grants["viewer"] = []
            invited_grants["editor"] = []
            invited_grants["admin"] = ["viewer", "editor", "admin"]
            invited_grants["owner"] = ["editor", "viewer", "admin"]

            can_delete = (
                invited_grantee.permission in invited_grants[granter.permission]
            )

            if not can_delete:
                return f"User cannot delete {invited_grantee.permission}", 403

            model.db.session.delete(invited_grantee)

            model.db.session.commit()

            return Response(status=204)

        user = model.User.query.get(user_id)

        if not user:
            return "user is not found", 404

        contributors = model.StudyContributor.query.filter(
            model.StudyContributor.study == study
        ).all()

        grantee = model.StudyContributor.query.filter(
            model.StudyContributor.user == user, model.StudyContributor.study == study
        ).first()

        if len(contributors) <= 1:
            return "the study must have at least one contributor", 422
        if grantee.user == granter.user:
            if granter.permission == "owner":
                return "you must transfer ownership before removing yourself", 422
            model.db.session.delete(grantee)
            model.db.session.commit()
            return Response(status=204)
        if not is_granted("delete_contributor", study):
            return (
                "Access denied, you are not authorized to change this permission",
                403,
            )
        can_delete = grantee.permission in grants[granter.permission]
        if not can_delete:
            return f"User cannot delete {grantee.permission}", 403
        model.db.session.delete(grantee)
        model.db.session.commit()
        return Response(status=204)


@api.route("/study/<study_id>/contributor/owner/<user_id>")
class AssignOwner(Resource):
    @api.doc("contributor update")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.expect(contributors_model)
    def put(self, study_id: int, user_id: int):
        """set owner based on the assigned permissions"""
        study = model.Study.query.get(study_id)
        if not is_granted("make_owner", study):
            return (
                "Access denied, you are not authorized to change this permission",
                403,
            )
        user = model.User.query.get(user_id)
        existing_contributor = model.StudyContributor.query.filter(
            model.StudyContributor.user == user,
            model.StudyContributor.study == study,
        ).first()
        existing_contributor.permission = "owner"
        existing_owner = model.StudyContributor.query.filter(
            model.StudyContributor.study == study,
            model.StudyContributor.permission == "owner",
        ).first()

        existing_owner.permission = "admin"
        model.db.session.commit()
        return Response(status=204)
