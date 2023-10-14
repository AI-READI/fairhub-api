"""API routes for study contact metadata"""
import typing

from email_validator import EmailNotValidError, validate_email
from flask import request
from flask_restx import Resource, fields
from jsonschema import FormatChecker, ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

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
        study_ = model.Study.query.get(study_id)

        study_contact_ = study_.study_contact

        sorted_study_contact = sorted(study_contact_, key=lambda x: x.created_at)

        return [s.to_dict() for s in sorted_study_contact if s.central_contact]

    def post(self, study_id: int):
        """Create study contact metadata"""
        def validate_is_valid_email(instance):
            print("within is_valid_email")
            email_address = instance
            print(email_address)
            try:
                validate_email(email_address)
                return True
            except EmailNotValidError as e:
                raise ValidationError("Invalid email address format") from e
        # Schema validation
        schema = {
            "type": "array",
            "additionalProperties": False,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "name",
                    "affiliation",
                    "phone",
                    "phone_ext",
                    "email_address"
                ],
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "affiliation": {"type": "string", "minLength": 1},
                    "role": {"type": "string", "minLength": 1},
                    "phone": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 30,
                        "pattern": "^[0-9-]+$",
                    },
                    "phone_ext": {
                        "type": "string", 
                        "minLength": 1, 
                        "pattern": "^[0-9-]+$", 
                        "errorMessage": "Invalid phone extension"
                    },
                    "email_address": {"type": "string", "format": "email"},
                    "central_contact": {"type": "boolean"},
                },
            },
            "minItems": 1,
        }

        format_checker = FormatChecker()
        format_checker.checks("email")(validate_is_valid_email)

        try:
            validate(instance=request.json, schema=schema, format_checker=format_checker)
        except ValidationError as e:
            return e.message, 400

        study = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study):
            return "Access denied, you can not delete study", 403
        data: typing.Union[dict, typing.Any] = request.json

        study_obj = model.Study.query.get(study_id)

        list_of_elements = []

        for i in data:
            if "id" in i and i["id"]:
                study_contact_ = model.StudyContact.query.get(i["id"])
                study_contact_.update(i)
                list_of_elements.append(study_contact_.to_dict())
            elif "id" not in i or not i["id"]:
                study_contact_ = model.StudyContact.from_data(study_obj, i, None, True)
                model.db.session.add(study_contact_)
                list_of_elements.append(study_contact_.to_dict())

        model.db.session.commit()

        return list_of_elements

    @api.route("/study/<study_id>/metadata/central-contact/<central_contact_id>")
    class StudyContactUpdate(Resource):
        """Study Contact Metadata"""

        def delete(self, study_id: int, central_contact_id: int):
            study = model.Study.query.get(study_id)
            if not is_granted("study_metadata", study):
                return "Access denied, you can not delete study", 403
            """Delete study contact metadata"""
            study_contact_ = model.StudyContact.query.get(central_contact_id)

            model.db.session.delete(study_contact_)
            model.db.session.commit()

            return study_contact_.to_dict()
