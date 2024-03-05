"""API routes for study sponsors and collaborators metadata"""

import typing

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_sponsors = api.model(
    "StudySponsors",
    {
        "responsible_party_type": fields.String(required=True),
        "responsible_party_investigator_first_name": fields.String(required=False),
        "responsible_party_investigator_last_name": fields.String(required=True),
        "responsible_party_investigator_title": fields.String(required=True),
        "responsible_party_investigator_identifier_value": fields.String(required=True),
        "responsible_party_investigator_identifier_scheme": fields.String(
            required=True
        ),
        "responsible_party_investigator_identifier_scheme_uri": fields.String(
            required=True
        ),
        "responsible_party_investigator_affiliation_name": fields.String(required=True),
        "responsible_party_investigator_affiliation_identifier_scheme": fields.String(
            required=True
        ),
        "responsible_party_investigator_affiliation_identifier_value": fields.String(
            required=True
        ),
        "responsible_party_investigator_affiliation_identifier_scheme_uri": fields.String(
            required=True
        ),
        "lead_sponsor_name": fields.String(required=True),
        "lead_sponsor_identifier": fields.String(required=True),
        "lead_sponsor_scheme": fields.String(required=True),
        "lead_sponsor_scheme_uri": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/sponsors")
class StudySponsorsResource(Resource):
    """Study Sponsors Metadata"""

    @api.doc("sponsors")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(study_sponsors)
    def get(self, study_id: int):
        """Get study sponsors metadata"""
        study_ = model.Study.query.get(study_id)

        study_sponsors_ = study_.study_sponsors

        return study_sponsors_.to_dict(), 200

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int):
        """Update study sponsors metadata"""
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "responsible_party_type",
                "lead_sponsor_name",
                "responsible_party_investigator_last_name",
                "responsible_party_investigator_first_name",
                "responsible_party_investigator_title",
            ],
            "properties": {
                "id": {"type": "string"},
                "responsible_party_type": {
                    "type": ["string", "null"],
                    "minLength": 1,
                    "enum": [
                        "Sponsor",
                        "Principal Investigator",
                        "Sponsor-Investigator",
                    ],
                },
                "responsible_party_investigator_first_name": {
                    "type": "string",
                },
                "responsible_party_investigator_last_name": {
                    "type": "string",
                },
                "responsible_party_investigator_title": {
                    "type": "string",
                },
                "responsible_party_investigator_identifier_value": {
                    "type": "string",
                    "minLength": 1,
                },
                "responsible_party_investigator_identifier_scheme": {
                    "type": "string",
                    "minLength": 1,
                },
                "responsible_party_investigator_identifier_scheme_uri": {
                    "type": "string",
                    "minLength": 1,
                },
                "responsible_party_investigator_affiliation_name": {
                    "type": "string",
                    "minLength": 1,
                },
                "responsible_party_investigator_affiliation_identifier_scheme": {
                    "type": "string",
                    "minLength": 1,
                },
                "responsible_party_investigator_affiliation_identifier_value": {
                    "type": "string",
                    "minLength": 1,
                },
                "responsible_party_investigator_affiliation_identifier_scheme_uri": {
                    "type": "string",
                    "minLength": 1,
                },
                "lead_sponsor_name": {"type": "string", "minLength": 1},
                "lead_sponsor_identifier": {"type": "string", "minLength": 1},
                "lead_sponsor_identifier_scheme": {"type": "string", "minLength": 1},
                "lead_sponsor_identifier_scheme_uri": {
                    "type": "string",
                    "minLength": 1,
                },
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: typing.Union[dict, typing.Any] = request.json
        if data["responsible_party_type"] in [
            "Principal Investigator",
            "Sponsor-Investigator",
        ]:
            if not data["responsible_party_investigator_last_name"]:
                return "Principal Investigator name is required", 400
            if not data["responsible_party_investigator_first_name"]:
                return "Principal Investigator name is required", 400

            if not data["responsible_party_investigator_title"]:
                return "Principal Investigator title is required", 400

            investigator_first_name = data["responsible_party_investigator_first_name"]
            investigator_last_name = data["responsible_party_investigator_last_name"]
            investigator_title = data["responsible_party_investigator_title"]

            if investigator_first_name == "":
                return "Principal Investigator first name cannot be empty", 400
            if investigator_last_name == "":
                return "Principal Investigator last name cannot be empty", 400
            if investigator_title == "":
                return "Principal Investigator title cannot be empty", 400

        study_ = model.Study.query.get(study_id)

        # Check user permissions
        if not is_granted("study_metadata", study_):
            return "Access denied, you can not modify study", 403

        study_.study_sponsors.update(data)

        model.db.session.commit()

        return study_.study_sponsors.to_dict(), 200
