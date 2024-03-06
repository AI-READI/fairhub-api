"""API routes for study contact metadata"""

import typing

from email_validator import EmailNotValidError, validate_email
from flask import Response, request
from flask_restx import Resource, fields
from jsonschema import FormatChecker, ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_contact = api.model(
    "StudyCentralContact",
    {
        "id": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "degree": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_scheme": fields.String(required=True),
        "identifier_scheme_uri": fields.String(required=True),
        "affiliation": fields.String(required=True),
        "affiliation_identifier": fields.String(required=True),
        "affiliation_identifier_scheme": fields.String(required=True),
        "affiliation_identifier_scheme_uri": fields.String(required=True),
        "phone": fields.String(required=True),
        "phone_ext": fields.String(required=True),
        "email_address": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/central-contact")
class StudyCentralContactResource(Resource):
    """Study Contact Metadata"""

    @api.doc("contact")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(study_contact)
    def get(self, study_id: int):
        """Get study contact metadata"""
        study_ = model.Study.query.get(study_id)

        study_central_contact_ = study_.study_central_contact
        # sorted_study_contact = sorted(study_central_contact_, key=lambda x: x.created_at)
        # return [s.to_dict() for s in sorted_study_contact if s.central_contact], 200

        return [s.to_dict() for s in study_central_contact_], 200

    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int):
        """Create study contact metadata"""

        def validate_is_valid_email(instance):
            email_address = instance

            try:
                validate_email(email_address)
                return True
            except EmailNotValidError as e:
                raise ValidationError("Invalid email address format") from e

        # Schema validation
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "first_name",
                    "last_name",
                    "affiliation",
                    "phone",
                    "phone_ext",
                    "email_address",
                ],
                "properties": {
                    "id": {"type": "string"},
                    "first_name": {"type": "string", "minLength": 1},
                    "last_name": {"type": "string", "minLength": 1},
                    "degree": {"type": "string", "minLength": 1},
                    "identifier": {"type": "string", "minLength": 1},
                    "identifier_scheme": {"type": "string", "minLength": 1},
                    "identifier_scheme_uri": {"type": "string", "minLength": 1},
                    "affiliation": {"type": "string", "minLength": 1},
                    "affiliation_identifier": {
                        "type": "string",
                        "minLength": 1,
                    },
                    "affiliation_identifier_scheme": {
                        "type": "string",
                    },
                    "affiliation_identifier_scheme_uri": {"type": "string"},
                    "phone": {"type": "string"},
                    "phone_ext": {"type": "string"},
                    "email_address": {"type": "string"},
                    # "email_address": {"type": "string", "format": "email"},
                },
            },
            "uniqueItems": True,
        }

        format_checker = FormatChecker()
        format_checker.checks("email")(validate_is_valid_email)

        try:
            validate(
                instance=request.json, schema=schema, format_checker=format_checker
            )
        except ValidationError as e:
            return e.message, 400

        study = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study):
            return "Access denied, you can not modify study", 403
        data: typing.Union[dict, typing.Any] = request.json

        study_obj = model.Study.query.get(study_id)

        list_of_elements = []

        for i in data:
            if "id" in i and i["id"]:
                study_central_contact_ = model.StudyCentralContact.query.get(i["id"])
                study_central_contact_.update(i)
                list_of_elements.append(study_central_contact_.to_dict())
            elif "id" not in i or not i["id"]:
                study_central_contact_ = model.StudyCentralContact.from_data(
                    study_obj, i
                )
                model.db.session.add(study_central_contact_)
                list_of_elements.append(study_central_contact_.to_dict())

        model.db.session.commit()

        return list_of_elements, 201


@api.route("/study/<study_id>/metadata/central-contact/<central_contact_id>")
class StudyCentralContactDelete(Resource):
    """Study Central Contact Metadata"""

    @api.doc("Delete Study contacts")
    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, central_contact_id: int):
        """Delete study central contact metadata"""
        study = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study):
            return "Access denied, you can not delete study", 403
        study_central_contact_ = model.StudyCentralContact.query.get(central_contact_id)

        model.db.session.delete(study_central_contact_)
        model.db.session.commit()

        return Response(status=204)
