"""API routes for study sponsors and collaborators metadata"""
from flask_restx import Resource, fields
from flask import request
from jsonschema import validate, ValidationError
from model import Study, db
from ..authentication import is_granted


from apis.study_metadata_namespace import api


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
        study_ = Study.query.get(study_id)

        study_sponsors_collaborators_ = study_.study_sponsors_collaborators

        return study_sponsors_collaborators_.to_dict()

    def put(self, study_id: int):
        """Update study sponsors metadata"""
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "responsible_party_type",
                "responsible_party_investigator_name",
                "responsible_party_investigator_title",
                "responsible_party_investigator_affiliation",
                "lead_sponsor_name",
            ],
            "properties": {
                "responsible_party_type": {"type": "string"},
                "responsible_party_investigator_name": {"type": "string"},
                "responsible_party_investigator_title": {"type": "string"},
                "responsible_party_investigator_affiliation": {"type": "string"},
                "lead_sponsor_name": {"type": "string"},
            }
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        study_ = Study.query.get(study_id)

        study_.study_sponsors_collaborators.update(request.json)

        db.session.commit()

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
        study_ = Study.query.get(study_id)

        study_collaborators_ = study_.study_sponsors_collaborators.collaborator_name

        return study_collaborators_

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int):
        """updating study collaborators"""
        # Schema validation
        schema = {
            "type": "array",
            "items": {"type": "string"},
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data = request.json
        study_obj = Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        study_obj.study_sponsors_collaborators.collaborator_name = data
        study_obj.touch()
        db.session.commit()
        return study_obj.study_sponsors_collaborators.collaborator_name
