from flask import request, g
from flask_restx import Namespace, Resource, fields

from model import Study, db, User, StudyContributor
from .authentication import is_granted

api = Namespace("Study", description="Study operations", path="/")


study_model = api.model(
    "Study",
    {
        "title": fields.String(required=True, default=""),
        "image": fields.String(required=True, default=""),
    },
)


@api.route("/study")
class Studies(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_model)
    def get(self):
        """this code ensure each user access and see only allowed studies"""
        # studies = Study.query.filter(
        #     Study.study_contributors.any(User.id == g.user.id)
        # ).all()
        # studies = Study.query.filter(User.id == g.user.id).all()
        study_contributors = StudyContributor.query.filter(
            StudyContributor.user_id == g.user.id
        ).all()  # Filter contributors where user_id matches the user's id
        study_ids = [contributor.study_id for contributor in study_contributors]

        studies = Study.query.filter(Study.id.in_(study_ids)).all()
        return [s.to_dict() for s in studies]

    @api.expect(study_model)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self):
        add_study = Study.from_data(request.json)
        db.session.add(add_study)
        study_id = add_study.id
        study_ = Study.query.get(study_id)
        study_contributor = StudyContributor.from_data(study_, g.user, "owner")
        db.session.add(study_contributor)
        db.session.commit()
        return study_.to_dict()


@api.route("/study/<study_id>")
class StudyResource(Resource):
    @api.doc("get study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study)
    def get(self, study_id: int):
        study1 = Study.query.get(study_id)
        return study1.to_dict()

    @api.expect(study_model)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int):
        update_study = Study.query.get(study_id)
        if not is_granted("update_study", update_study):
            return "Access denied, you can not modify", 403

        update_study.update(request.json)
        db.session.commit()
        return update_study.to_dict()

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int):
        study = Study.query.get(study_id)
        if not is_granted("delete_study", study):
            return "Access denied, you can not delete study", 403
        for d in study.dataset:
            for version in d.dataset_versions:
                version.participants.clear()
        for d in study.dataset:
            for version in d.dataset_versions:
                db.session.delete(version)
            db.session.delete(d)
        for p in study.participants:
            db.session.delete(p)
        db.session.delete(study)
        db.session.commit()
        studies = Study.query.filter(
            Study.study_contributors.any(User.id == g.user.id)
        ).all()
        return [s.to_dict() for s in studies], 201
