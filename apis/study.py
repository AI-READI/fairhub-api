from flask import request
from flask_restx import Namespace, Resource, fields, reqparse

from model import Study, db

api = Namespace("Study", description="Study operations", path="/")

owner = api.model(
    "Owner",
    {
        "id": fields.String(required=True),
        "affiliations": fields.String(required=True),
        "email": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "orcid": fields.String(required=True),
        "roles": fields.List(fields.String, required=True),
        "permission": fields.String(required=True),
        "status": fields.String(required=True),
    },
)

study = api.model(
    "Study",
    {
        "id": fields.String(required=True),
        "title": fields.String(required=True),
        "image": fields.String(required=True),
        "last_updated": fields.String(required=True),
        "owner": fields.Nested(owner, required=True),
    },
)


@api.route("/study")
class Studies(Resource):
    parser_study = reqparse.RequestParser(bundle_errors=True)
    parser_study.add_argument(
        "title", type=str, required=True, location="json", help="The title of the Study"
    )
    parser_study.add_argument(
        "image",
        type=list,
        required=True,
        location="json",
        help="The image for the Study",
    )

    @api.doc(description="Return a list of all studies")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study)
    def get(self):
        studies = Study.query.all()
        return [s.to_dict() for s in studies]

    @api.doc(description="Create a new study")
    @api.expect(parser_study)
    def post(self):
        print(request)
        add_study = Study.from_data(request.json)
        db.session.add(add_study)
        db.session.commit()
        return add_study.to_dict()


@api.route("/study/<study_id>")
class StudyResource(Resource):
    @api.doc(description="Get a study's details")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study)
    def get(self, study_id: int):
        study1 = Study.query.get(study_id)
        return study1.to_dict()

    @api.doc(description="Update a study's details")
    def put(self, study_id: int):
        update_study = Study.query.get(study_id)
        update_study.update(request.json)
        db.session.commit()
        return update_study.to_dict()

    @api.doc(description="Delete a study")
    def delete(self, study_id: int):
        delete_study = Study.query.get(study_id)
        for d in delete_study.dataset:
            print(d)
            for version in d.dataset_versions:
                version.participants.clear()
        for d in delete_study.dataset:
            for version in d.dataset_versions:
                db.session.delete(version)
            db.session.delete(d)
        for p in delete_study.participants:
            db.session.delete(p)
        # delete study_description
        db.session.delete(delete_study.study_description)
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
