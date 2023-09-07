from flask_restx import Namespace, Resource, fields
from model import Study, db, StudyAvailableIpd
from flask import request
from flask_restx import reqparse
from apis.study_metadata_namespace import api

study_available = api.model(
    "StudyAvailable",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "type": fields.String(required=True),
        "comment": fields.String(required=True),
        "url": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/available-ipd")
class StudyAvailableResource(Resource):
    @api.doc("available")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    #@api.marshal_with(study_available)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_available_ipd = study_.study_available_ipd
        return [s.to_dict() for s in study_available_ipd]

    @api.doc("update available")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(study_available)
    def post(self, study_id: int):
        # parser = reqparse.RequestParser()
        # parser.add_argument("username", type=str, required=True)
        # parser.add_argument("password", type=str, required=True)
        # parser.add_argument("username", type=str, required=True)
        # parser.add_argument("password", type=str, required=True)
        # parser.add_argument("password", type=str, required=True)
        # args = parser.parse_args()

        data = request.json
        study_obj = Study.query.get(study_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                study_available_ipd_ = StudyAvailableIpd.query.get(i["id"])
                study_available_ipd_.update(i)
                list_of_elements.append(study_available_ipd_.to_dict())
            elif "id" not in i or not i["id"]:
                study_available_ipd_ = StudyAvailableIpd.from_data(study_obj, i)
                db.session.add(study_available_ipd_)
                list_of_elements.append(study_available_ipd_.to_dict())
        db.session.commit()
        return list_of_elements


@api.route("/study/<study_id>/metadata/available-ipd/<available_ipd_id>")
class StudyLocationUpdate(Resource):
    def delete(self, study_id: int, available_ipd_id: int):
        study_available_ = StudyAvailableIpd.query.get(available_ipd_id)
        db.session.delete(study_available_)
        db.session.commit()
        return 204
