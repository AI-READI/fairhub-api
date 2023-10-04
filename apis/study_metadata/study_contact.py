from flask_restx import Namespace, Resource, fields
from model import Study, db, StudyContact
from flask import request
from apis.study_metadata_namespace import api

study_contact = api.model(
    "StudyContact",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "affiliation": fields.String(required=True),
        "role": fields.String(required=True),
        "phone": fields.String(required=True),
        "phone_ext": fields.String(required=True),
        "email_address": fields.String(required=True),
        "central_contact": fields.Boolean(required=True),
    },
)


@api.route("/study/<study_id>/metadata/central-contact")
class StudyContactResource(Resource):
    @api.doc("contact")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(study_contact)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_contact_ = study_.study_contact
        sorted_study_contact = sorted(study_contact_, key=lambda x: x.created_at)
        return [s.to_dict() for s in sorted_study_contact if s.central_contact]

    def post(self, study_id: int):
        data = request.json
        study_obj = Study.query.get(study_id)
        for i in data:
            if "id" in i and i["id"]:
                study_contact_ = StudyContact.query.get(i["id"])
                study_contact_.update(i)
            else:
                study_contact_ = StudyContact.from_data(study_obj, i, None, True)
                db.session.add(study_contact_)
        list_of_elements = [study_contact_.to_dict()]
        db.session.commit()
        print(list_of_elements)
        return list_of_elements

    @api.route("/study/<study_id>/metadata/central-contact/<central_contact_id>")
    class StudyContactUpdate(Resource):
        def delete(self, study_id: int, central_contact_id: int):
            study_contact_ = StudyContact.query.get(central_contact_id)
            db.session.delete(study_contact_)
            db.session.commit()
            return study_contact_.to_dict()
