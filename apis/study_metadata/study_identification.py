"""API routes for study identification metadata"""
import typing

from flask import request, Response
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_identification = api.model(
    "StudyIdentification",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_type": fields.String(required=True),
        "identifier_domain": fields.String(required=True),
        "identifier_link": fields.String(required=True),
        "secondary": fields.Boolean(required=True),
    },
)


@api.route("/study/<study_id>/metadata/identification")
class StudyIdentificationResource(Resource):
    """Study Identification Metadata"""

    @api.doc("identification")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    # @api.marshal_with(study_identification)
    def get(self, study_id: int):
        """Get study identification metadata"""
        study_ = model.Study.query.get(study_id)
        identifiers = model.Identifiers(study_)
        return identifiers.to_dict()

    @api.doc("identification add")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.expect(study_identification)
    def post(self, study_id: int):
        """Create study identification metadata"""
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "primary": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "identifier": {"type": "string", "minLength": 1},
                        "identifier_type": {
                            "type": "string",
                            "minLength": 1,
                        },
                        "identifier_domain": {
                            "type": "string",
                        },
                        "identifier_link": {
                            "type": "string",
                        },
                    },
                },
                "secondary": {
                    "type": "array",
                },
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not modify study", 403

        data: typing.Union[dict, typing.Any] = request.json
        identifiers = [i for i in study_obj.study_identification if not i.secondary]
        primary_identifier = identifiers[0] if len(identifiers) else None

        primary: dict = data["primary"]

        if primary_identifier:
            primary_identifier.update(primary)
        else:
            study_identification_ = model.StudyIdentification.from_data(
                study_obj, primary, False
            )
            model.db.session.add(study_identification_)

        for i in data["secondary"]:
            i["secondary"] = True
            if "id" in i and i["id"]:
                study_identification_ = model.StudyIdentification.query.get(i["id"])
                study_identification_.update(i)
            else:
                study_identification_ = model.StudyIdentification.from_data(
                    study_obj, i, True
                )
                model.db.session.add(study_identification_)

        model.db.session.commit()

        final_identifiers = model.Identifiers(study_obj)

        return final_identifiers.to_dict()

    @api.route("/study/<study_id>/metadata/identification/<identification_id>")
    class StudyIdentificationdUpdate(Resource):
        """Study Identification Metadata"""

        @api.doc("Delete Study Identifications")
        @api.response(204, "Success")
        @api.response(400, "Validation Error")
        def delete(self, study_id: int, identification_id: int):
            """Delete study identification metadata"""
            study = model.Study.query.get(study_id)
            if not is_granted("study_metadata", study):
                return "Access denied, you can not delete study", 403

            study_identification_ = model.StudyIdentification.query.get(
                identification_id
            )
            if not study_identification_.secondary:
                return "primary identifier can not be deleted", 400

            model.db.session.delete(study_identification_)
            model.db.session.commit()

            return Response(status=204)
