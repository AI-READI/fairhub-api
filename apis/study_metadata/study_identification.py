from flask_restx import Namespace, Resource, fields
from model import Study, db, StudyIdentification
from flask import request


from apis.study_metadata_namespace import api


study_identification = api.model(
    "StudyIdentification",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_type": fields.String(required=True),
        "identifier_domain": fields.String(required=True),
        "identifier_link": fields.String(required=True),
        "secondary": fields.Boolean(required=True),
    },
)


@api.route("/study/<study_id>/metadata/identification")
class StudyIdentificationResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_identification)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_identification_ = study_.study_identification
        return [s.to_dict() for s in study_identification_]

    def post(self, study_id: int):
        data = request.json
        study_obj = Study.query.get(study_id)
        list_of_elements = []
        for i in data:
            if 'id' in i and i["id"]:
                study_identification_ = StudyIdentification.query.get(i["id"])
                study_identification_.update(i)
                list_of_elements.append(study_identification_.to_dict())
            elif "id" not in i or not i["id"]:
                study_identification_ = StudyIdentification.from_data(study_obj, i)
                db.session.add(study_identification_)
                list_of_elements.append(study_identification_.to_dict())
        db.session.commit()
        return list_of_elements

    # @api.route("/study/<study_id>/metadata/available_ipd/<available_ipd_id>")
    # class StudyIdentificationdUpdate(Resource):
    #     def put(self, study_id: int, available_ipd_id: int):
    #         study_available_ipd_ = StudyIdentification.query.get(available_ipd_id)
    #         study_available_ipd_.update(request.json)
    #         db.session.commit()
    #         return study_available_ipd_.to_dict()
