"""API routes for study identification metadata"""
import typing

from flask import request
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
                        "identifier": {"type": "string"},
                        "identifier_type": {"type": "string"},
                        "identifier_domain": {"type": "string"},
                        "identifier_link": {"type": "string"},
                    },
                },
                "secondary": {
                    "type": "array",
                },
            }
        }
        
        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400
        
        data: typing.Union[dict, typing.Any] = request.json

        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        primary: dict = data["primary"]
        primary["secondary"] = False

        if "id" in primary and primary["id"]:
            study_identification_ = model.StudyIdentification.query.get(primary["id"])
            study_identification_.update(primary)
        elif "id" not in primary or not primary["id"]:
            study_identification_ = model.StudyIdentification.from_data(
                study_obj, primary, False
            )
            model.db.session.add(study_identification_)

        for i in data["secondary"]:
            i["secondary"] = True

            if "id" in i and i["id"]:
                study_identification_ = model.StudyIdentification.query.get(i["id"])
                study_identification_.update(i)
            elif "id" not in i or not i["id"]:
                study_identification_ = model.StudyIdentification.from_data(
                    study_obj, i, True
                )
                model.db.session.add(study_identification_)

        model.db.session.commit()

        identifiers = model.Identifiers(study_obj)

        return identifiers.to_dict()

    @api.route("/study/<study_id>/metadata/identification/<identification_id>")
    class StudyIdentificationdUpdate(Resource):
        """Study Identification Metadata"""

        def delete(self, study_id: int, identification_id: int):
            """Delete study identification metadata"""
            study = model.Study.query.get(study_id)
            if not is_granted("study_metadata", study):
                return "Access denied, you can not delete study", 403
            study_identification_ = model.StudyIdentification.query.get(
                identification_id
            )

            if not study_identification_.secondary:
                return 400, "primary identifier can not be deleted"

            model.db.session.delete(study_identification_)
            model.db.session.commit()

            return 204
