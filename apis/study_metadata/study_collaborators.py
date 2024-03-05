"""API routes for study collaborators metadata"""

import typing

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted


study_collaborators = api.model(
    "StudyCollaborators",
    {
        "collaborator_name": fields.List(fields.String, required=True),
    },
)



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
        study_collaborators_ = study_.study_sponsors_collaborators

        return [collab.to_dict() for collab in study_collaborators_], 200

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
            return "Access denied, you can not modify study", 403

        study_obj.study_collaborators.update(data)

        model.db.session.commit()
        return study_obj.study_sponsors_collaborators.collaborator_name, 200
