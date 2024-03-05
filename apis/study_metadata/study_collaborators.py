"""API routes for study collaborators metadata"""

import typing

from flask import Response, request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_collaborators = api.model(
    "StudyCollaborators",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "identifier": fields.String(required=True),
        "scheme": fields.String(required=True),
        "scheme_uri": fields.String(required=True),
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
        study_collaborators_ = study_.study_collaborators

        return [collab.to_dict() for collab in study_collaborators_], 200

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int):
        """updating study collaborators"""
        # Schema validation
        schema = {
            "type": "array",
            "additionalProperties": False,
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "identifier": {"type": "string"},
                    "scheme": {"type": "string"},
                    "scheme_uri": {"type": "string"},
                },
                "required": ["name", "identifier", "scheme", "scheme_uri"],
            },
        }
        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: typing.Union[dict, typing.Any] = request.json

        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not modify study", 403

        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                study_collaborators_ = model.StudyCollaborators.query.get(i["id"])
                study_collaborators_.update(i)
            else:
                study_collaborators_ = model.StudyCollaborators.from_data(study_obj, i)
                model.db.session.add(study_collaborators_)
            list_of_elements.append(study_collaborators_.to_dict())
        model.db.session.commit()

        return list_of_elements, 201


@api.route("/study/<study_id>/metadata/collaborators/<collaborator_id>")
class StudyLocationUpdate(Resource):
    """delete Study Collaborators Metadata"""

    @api.doc("delete study collaborators")
    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    def delete(self, study_id: int, collaborator_id: int):
        """Delete study collaborators metadata"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        study_collaborators_ = model.StudyCollaborators.query.get(collaborator_id)

        model.db.session.delete(study_collaborators_)

        model.db.session.commit()

        return Response(status=204)
