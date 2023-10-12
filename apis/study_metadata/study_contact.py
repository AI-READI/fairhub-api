"""API routes for study contact metadata"""
from flask_restx import Resource, fields
from flask import request
from model import Study, db, StudyContact
from apis.study_metadata_namespace import api
from ..authentication import is_granted, is_study_metadata
from jsonschema import validate, ValidationError


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
    """Study Contact Metadata"""

    @api.doc("contact")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(study_contact)
    def get(self, study_id: int):
        """Get study contact metadata"""
        study_ = Study.query.get(study_id)

        study_contact_ = study_.study_contact

        sorted_study_contact = sorted(study_contact_, key=lambda x: x.created_at)

        return [s.to_dict() for s in sorted_study_contact if s.central_contact]

    def post(self, study_id: int):
        """Create study contact metadata"""
        # Schema validation
        schema = {
            "type": "array",
            "additionalProperties": False,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "affiliation": {"type": "string"},
                    "role": {"type": "string"},
                    "phone": {"type": "string"},
                    "phone_ext": {"type": "string"},
                    "email_address": {"type": "string"},
                    "central_contact": {"type": "boolean"},
                },
                "required": [
                    "name",
                    "affiliation",
                    "role",
                    "phone",
                    "phone_ext",
                    "email_address",
                    "central_contact",
                ],
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        study = Study.query.get(study_id)
        if not is_granted("study_metadata", study):
            return "Access denied, you can not delete study", 403
        data = request.json

        study_obj = Study.query.get(study_id)

        list_of_elements = []

        for i in data:
            if "id" in i and i["id"]:
                study_contact_ = StudyContact.query.get(i["id"])
                study_contact_.update(i)
                list_of_elements.append(study_contact_.to_dict())
            elif "id" not in i or not i["id"]:
                study_contact_ = StudyContact.from_data(study_obj, i, None, True)
                db.session.add(study_contact_)
                list_of_elements.append(study_contact_.to_dict())

        db.session.commit()

        return list_of_elements

    @api.route("/study/<study_id>/metadata/central-contact/<central_contact_id>")
    class StudyContactUpdate(Resource):
        """Study Contact Metadata"""

        def delete(self, study_id: int, central_contact_id: int):
            study = Study.query.get(study_id)
            if not is_granted("study_metadata", study):
                return "Access denied, you can not delete study", 403
            """Delete study contact metadata"""
            study_contact_ = StudyContact.query.get(central_contact_id)

            db.session.delete(study_contact_)
            db.session.commit()

            return study_contact_.to_dict()
