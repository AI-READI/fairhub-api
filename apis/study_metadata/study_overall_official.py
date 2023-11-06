"""API routes for study overall official metadata"""
import typing

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_overall_official = api.model(
    "StudyOverallOfficial",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "affiliation": fields.String(required=True),
        "role": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/overall-official")
class StudyOverallOfficialResource(Resource):
    """Study Overall Official Metadata"""

    @api.doc("overall_official")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    # @api.marshal_with(study_overall_official)
    def get(self, study_id: int):
        """Get study overall official metadata"""
        study_ = model.Study.query.get(study_id)

        study_overall_official_ = study_.study_overall_official

        # sorted_by_date = sorted([i.created_at for i in study_overall_official_])

        sorted_study_overall = sorted(
            study_overall_official_, key=lambda x: x.created_at
        )

        return [i.to_dict() for i in sorted_study_overall]

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int):
        """Create study overall official metadata"""
        # Schema validation
        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string", "minLength": 1},
                    "affiliation": {"type": "string", "minLength": 1},
                    "role": {
                        "type": "string",
                        "enum": [
                            "Study Chair",
                            "Study Director",
                            "Study Principal Investigator",
                        ],
                    },
                },
                "required": ["name", "affiliation", "role"],
            },
            "uniqueItems": True,
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: typing.Union[dict, typing.Any] = request.json
        study_obj = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                study_overall_official_ = model.StudyOverallOfficial.query.get(i["id"])
                study_overall_official_.update(i)
                list_of_elements.append(study_overall_official_.to_dict())
            elif "id" not in i or not i["id"]:
                study_overall_official_ = model.StudyOverallOfficial.from_data(
                    study_obj, i
                )
                model.db.session.add(study_overall_official_)
                list_of_elements.append(study_overall_official_.to_dict())

        model.db.session.commit()

        return list_of_elements

    @api.route("/study/<study_id>/metadata/overall-official/<overall_official_id>")
    class StudyOverallOfficialUpdate(Resource):
        @api.response(200, "Success")
        @api.response(400, "Validation Error")
        def delete(self, study_id: int, overall_official_id: int):
            """Delete study overall official metadata"""
            study_obj = model.Study.query.get(study_id)
            if not is_granted("study_metadata", study_obj):
                return "Access denied, you can not delete study", 403
            study_overall_official_ = model.StudyOverallOfficial.query.get(
                overall_official_id
            )
            model.db.session.delete(study_overall_official_)
            model.db.session.commit()

            return 204
