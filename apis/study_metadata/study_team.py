"""API routes for study sponsors and collaborators metadata"""

import typing

from flask import request
from flask_restx import Resource, fields

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_sponsors = api.model(
    "StudySponsors",
    {
        "responsible_party_type": fields.String(required=False),
        "responsible_party_investigator_first_name": fields.String(required=True),
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
        "lead_sponsor_identifier_scheme": fields.String(required=True),
        "lead_sponsor_identifier_scheme_uri": fields.String(required=True),
    },
)

study_collaborators = api.model(
    "StudyCollaborators",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "identifier": fields.String(required=True),
        "scheme": fields.String(required=True),
        "scheme_uri": fields.String(required=True),
        "created_at": fields.Integer(required=True),
    },
)


@api.route("/study/<study_id>/metadata/team")
class StudySponsorsResource(Resource):
    """Study team Metadata"""

    @api.doc("sponsors")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(
    #     {
    #         "sponsors": study_sponsors,
    #         "collaborators": study_collaborators
    #     }
    # )
    def get(self, study_id: int):
        """Get study team metadata"""
        study_ = model.Study.query.get(study_id)

        study_sponsors_ = study_.study_sponsors
        study_collaborators_ = study_.study_collaborators
        # print(study_sponsors_.to_dict(),"ggg")

        return {
            "sponsors": study_sponsors_.to_dict(),
            "collaborators": [collab.to_dict() for collab in study_collaborators_],
        }
        200

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int):
        """Update study team metadata"""
        # Schema validation
        # schema = {
        #     "type": "object",
        #     "additionalProperties": False,
        #     "properties": {
        #         "collaborators": {
        #             "type": "array",
        #             "additionalProperties": False,
        #             "items": {
        #                 "type": "object",
        #                 "properties": {
        #                     "id": {"type": "string"},
        #                     "name": {"type": "string"},
        #                     "identifier": {"type": "string"},
        #                     "identifier_scheme": {"type": "string"},
        #                     "identifier_scheme_uri": {"type": "string"},
        #                 },
        #                 "required": [
        #                     "name",
        #                     "identifier",
        #                     "identifier_scheme",
        #                 ],
        #             },
        #         },
        #         "sponsors":
        #             {
        #             "type": "object",
        #             "additionalProperties": False,
        #              "properties": {
        #                 "responsible_party_type": {
        #                 "type": ["string", "null"],
        #                 "enum": [
        #                     "Sponsor",
        #                     "Principal Investigator",
        #                     "Sponsor-Investigator",
        #                 ],
        #             },
        #                 "responsible_party_investigator_first_name": {
        #                     "type": "string",
        #                 },
        #                 "responsible_party_investigator_last_name": {
        #                     "type": "string",
        #                 },
        #                 "responsible_party_investigator_title": {
        #                     "type": "string",
        #                 },
        #                 "responsible_party_investigator_identifier_value": {
        #                     "type": "string",
        #                 },
        #                 "responsible_party_investigator_identifier_scheme": {
        #                     "type": "string",
        #                 },
        #                 "responsible_party_investigator_identifier_scheme_uri": {
        #                     "type": "string",
        #                 },
        #                 "responsible_party_investigator_affiliation_name": {
        #                     "type": "string",
        #                 },
        #                 "responsible_party_investigator_affiliation_identifier_scheme": {
        #                     "type": "string",
        #                 },
        #                 "responsible_party_investigator_affiliation_identifier_value": {
        #                     "type": "string",
        #                 },
        #                 "responsible_party_investigator_affiliation_identifier_scheme_uri": {
        #                     "type": "string",
        #                 },
        #                 "lead_sponsor_name": {"type": "string"},
        #                 "lead_sponsor_identifier": {"type": "string"},
        #                 "lead_sponsor_identifier_scheme": {"type": "string"},
        #                 "lead_sponsor_identifier_scheme_uri": {
        #                 "type": "string",
        #             },
        #         },
        #              "required": [
        #                 "responsible_party_type",
        #                 "lead_sponsor_name",
        #                 "responsible_party_investigator_last_name",
        #                 "responsible_party_investigator_first_name",
        #                 "responsible_party_investigator_title",
        #             ],
        #             }
        #     }
        # }
        #
        # try:
        #     validate(request.json, schema)
        # except ValidationError as e:
        #     return e.message, 400
        data: typing.Union[dict, typing.Any] = request.json

        if data["sponsors"]["responsible_party_type"] in [
            "Principal Investigator",
            "Sponsor-Investigator",
        ]:
            if not data["sponsors"]["responsible_party_investigator_last_name"]:
                return "Principal Investigator name is required", 400
            if not data["sponsors"]["responsible_party_investigator_first_name"]:
                return "Principal Investigator name is required", 400

            if not data["sponsors"]["responsible_party_investigator_title"]:
                return "Principal Investigator title is required", 400

            investigator_first_name = data["sponsors"][
                "responsible_party_investigator_first_name"
            ]
            investigator_last_name = data["sponsors"][
                "responsible_party_investigator_last_name"
            ]
            investigator_title = data["sponsors"][
                "responsible_party_investigator_title"
            ]

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

        list_of_elements = []
        for i in data["collaborators"]:
            if "id" in i and i["id"]:
                study_collaborators_ = model.StudyCollaborators.query.get(i["id"])
                study_collaborators_.update(i)
            else:
                study_collaborators_ = model.StudyCollaborators.from_data(study_, i)
                model.db.session.add(study_collaborators_)
            list_of_elements.append(study_collaborators_.to_dict())

        study_.study_sponsors.update(data["sponsors"])

        model.db.session.commit()

        return {
            "collaborators": list_of_elements,
            "sponsors": study_.study_sponsors.to_dict(),
        }, 201