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
        "id": fields.String(required=True),
        "responsible_party_type": fields.String(required=True),
        "responsible_party_investigator_name": fields.String(required=True),
        "responsible_party_investigator_title": fields.String(required=True),
        "responsible_party_investigator_affiliation": fields.String(required=True),
        "lead_sponsor_name": fields.String(required=True),
    },
)


study_collaborators = api.model(
    "StudyCollaborators",
    {
        "collaborator_name": fields.List(fields.String, required=True),
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

        study_sponsors_collaborators_ = study_.study_sponsors_collaborators

        return study_sponsors_collaborators_.to_dict()

    def put(self, study_id: int):
        """Update study sponsors metadata"""
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["responsible_party_type"],
            "properties": {
                "responsible_party_type": {
                    "type": "string",
                    "minLength": 1,
                    "enum": [
                        "Sponsor",
                        "Principal Investigator",
                        "Sponsor-Investigator",
                    ],
                },
                "responsible_party_investigator_name": {
                    "type": "string",
                    "minLength": 1,
                },
                "responsible_party_investigator_title": {
                    "type": "string",
                    "minLength": 1,
                },
                "responsible_party_investigator_affiliation": {
                    "type": "string",
                    "minLength": 1,
                },
                "lead_sponsor_name": {"type": "string", "minLength": 1},
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data = request.json
        if data["responsible_party_type"] in [
            "Principal Investigator",
            "Sponsor-Investigator",
        ]:
            if not data["responsible_party_investigator_name"]:
                return ("Principal Investigator name is required", 400)

            if not data["responsible_party_investigator_title"]:
                return ("Principal Investigator title is required", 400)

            if not data["responsible_party_investigator_affiliation"]:
                return ("Principal Investigator affiliation is required", 400)

            investigator_name = data["responsible_party_investigator_name"]
            investigator_title = data["responsible_party_investigator_title"]
            investigator_affiliation = data["responsible_party_investigator_affiliation"]

            if investigator_name == "":
                return ("Principal Investigator name cannot be empty", 400)
            if investigator_title == "":
                return ("Principal Investigator title cannot be empty", 400)
            if investigator_affiliation == "":
                return ("Principal Investigator affiliation cannot be empty", 400)

        study_ = model.Study.query.get(study_id)

        study_.study_sponsors_collaborators.update(request.json)

        model.db.session.commit()

        return study_.study_sponsors_collaborators.to_dict()


@api.route("/study/<study_id>/metadata/collaborators")
class StudyCollaboratorsResource(Resource):
    """Study Collaborators Metadata"""

    @api.doc("collaborators")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(study_collaborators)
    def get(self, study_id: int):
        """Get study collaborators metadata"""
        study_ = model.Study.query.get(study_id)

        study_collaborators_ = study_.study_sponsors_collaborators.collaborator_name

        return study_collaborators_

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int):
        """updating study collaborators"""
        # Schema validation
        schema = {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: typing.Union[dict, typing.Any] = request.json
        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        study_obj.study_sponsors_collaborators.collaborator_name = data
        study_obj.touch()
        model.db.session.commit()
        return study_obj.study_sponsors_collaborators.collaborator_name
