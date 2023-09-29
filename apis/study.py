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
    # @api.marshal_with(study)
    def get(self):
        """this code ensure each user access and see only allowed studies"""
        studies = Study.query.filter(
            Study.study_contributors.any(User.id == g.user.id)).all()
        return [s.to_dict() for s in studies]

    @api.expect(study_model)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self):
        add_study = Study.from_data(request.json)
        db.session.add(add_study)
        db.session.commit()
        study_id = add_study.id
        study_ = Study.query.get(study_id)
        study_contributor = StudyContributor.from_data(study_, g.user, "owner")
        db.session.add(study_contributor)
        db.session.commit()
        return 204


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
        if is_granted("viewer", study_id):
            return "Access denied, you can not modify", 403
        update_study = Study.query.get(study_id)
        update_study.update(request.json)
        db.session.commit()
        return update_study.to_dict()

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int):
        # if not is_granted("owner", study_id):
        #     return "Access denied, you can not delete study", 403
        delete_study = Study.query.get(study_id)
        for d in delete_study.dataset:
            for version in d.dataset_versions:
                version.participants.clear()
        for d in delete_study.dataset:
            for version in d.dataset_versions:
                db.session.delete(version)
            db.session.delete(d)
        for p in delete_study.participants:
            db.session.delete(p)
        for c in delete_study.study_contributors:
            db.session.delete(c)
        db.session.delete(delete_study)
        db.session.commit()
        return "", 204


# @api.route("/view-profile", methods=["GET"])
# def viewProfile():
#     return jsonify(dic)
#


# @study.route("/view-profile", methods=["POST"])
# def update_user_profile():
#     data = request.json
#     if data is not None:
#     return jsonify(data), 201
#
