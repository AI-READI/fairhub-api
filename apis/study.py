from flask import request
from flask_restx import Namespace, Resource, fields

from model import Study, db, User

api = Namespace("study", description="study operations", path="/")

owner = {
    "id": str,
    "affiliations": str,
    "email": str,
    "first_name": str,
    "last_name": str,
    "orcid": str,
    "roles": [],
    "permission": str,
    "status": str,
}
study = api.model(
    "Study",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "title": fields.String(required=True),
        "description": fields.String(required=True),
        "image": fields.String(required=True),
        "size": fields.String(required=True),
        "keywords": fields.String(required=True),
        "last_updated": fields.String(required=True),
        "owner": fields.Nested(owner, required=True),
    },
)


@api.route("/study")
class Studies(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.param("id", "The study identifier")
    @api.marshal_list_with(study)
    def get(self):
        studies = Study.query.all()
        return [s.to_dict() for s in studies]

    def post(self):
        add_study = Study.from_data(request.json)
        db.session.add(add_study)
        db.session.commit()
        return add_study.to_dict()


@api.route("/study/<study_id>")
class StudyResource(Resource):
    @api.doc("update study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.param("id", "The study identifier")
    @api.marshal_with(study)
    def get(self, study_id: int):
        study1 = Study.query.get(study_id)
        return study1.to_dict()

    def put(self, study_id: int):
        update_study = Study.query.get(study_id)
        # if not addStudy.validate():
        #     return 'error', 422
        update_study.update(request.json)
        db.session.commit()
        return update_study.to_dict()

    def delete(self, study_id: int):
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
        db.session.delete(delete_study)
        db.session.commit()
        return "", 204


# @api.route("/viewProfile", methods=["GET"])
# def viewProfile():
#     dic = {
#         "username": "admin",
#         "email": "aydan.gasimova2@gmail.com",
#         "fullname": "Aydan Gasimova",
#         "image": f" https://api.dicebear.com/5.x/shapes/svg?seed=$"
#         f"{str(random.randint(0,1000))}",
#         "institution": "CALMI2",
#         "location": "San Diego, CA",
#         "password": "admin",
#         "timezone": "(GMT-11:00) Midway Island",
#     }
#     return jsonify(dic)
#


# @study.route("/viewProfile", methods=["POST"])
# def update_user_profile():
#     data = request.json
#
#     if data is not None:
#         data["id"] = 3
#
#     return jsonify(data), 201
#
