from flask_restx import Namespace, Resource, fields
from model import Study, db, StudyContact
from flask import request
from apis.study_metadata_namespace import api

study_contact = api.model(
    "StudyContact",
    {
        "id": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "affiliation": fields.String(required=True),
        "role": fields.String(required=True),
        "phone": fields.String(required=True),
        "phone_ext": fields.String(required=True),
        "email_address": fields.String(required=True),
        "central_contact": fields.Boolean(required=True),
    },
)


@api.route("/study/<study_id>/metadata/contact")
class StudyContactResource(Resource):
    @api.doc("contact")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(study_contact)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_contact_ = study_.study_contact
        return [s.to_dict() for s in study_contact_]

    def post(self, study_id: int):
        data = request.json
        study_obj = Study.query.get(study_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                study_contact_ = StudyContact.query.get(i["id"])
                study_contact_.update(i)
                list_of_elements.append(study_contact_.to_dict())
            elif "id" not in i or not i["id"]:
                study_contact_ = StudyContact.from_data(study_obj, i)
                db.session.add(study_contact_)
                list_of_elements.append(study_contact_.to_dict())
        db.session.commit()
        return list_of_elements

    # @api.route("/study/<study_id>/metadata/arm/<arm_id>")
    # class StudyArmUpdate(Resource):
    #     def put(self, study_id: int, arm_id: int):
    #         study_arm_ = StudyContact.query.get(arm_id)
    #         study_arm_.update(request.json)
    #         db.session.commit()
    #         return study_arm_.to_dict()