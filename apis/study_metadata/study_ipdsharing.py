"""API routes for study ipdsharing metadata"""

import typing

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.study_metadata_namespace import api

from ..authentication import is_granted

study_ipdsharing = api.model(
    "StudyIpdsharing",
    {
        "id": fields.String(required=True),
        "ipd_sharing": fields.String(required=True),
        "ipd_sharing_description": fields.String(required=True),
        "ipd_sharing_info_type_list": fields.List(fields.String, required=True),
        "ipd_sharing_time_frame": fields.String(required=True),
        "ipd_sharing_access_criteria": fields.String(required=True),
        "ipd_sharing_url": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/ipdsharing")
class StudyIpdsharingResource(Resource):
    """Study Ipd sharing Metadata"""

    @api.doc("ipdsharing")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_ipdsharing)
    def get(self, study_id: int):
        """Get study ipdsharing metadata"""
        study_ = model.Study.query.get(study_id)

        return study_.study_ipdsharing.to_dict(), 200

    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int):
        """Create study ipdsharing metadata"""
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "ipd_sharing": {"type": "string", "enum": ["Yes", "No", "Undecided"]},
                "ipd_sharing_description": {"type": "string"},
                "ipd_sharing_info_type_list": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "Study Protocol",
                            "Statistical Analysis Plan (SAP)",
                            "Informed Consent Form (ICF)",
                            "Clinical Study Report (CSR)",
                            "Analytical Code",
                        ],
                    },
                    "uniqueItems": True,
                },
                "ipd_sharing_time_frame": {"type": "string"},
                "ipd_sharing_access_criteria": {"type": "string"},
                "ipd_sharing_url": {"type": "string", "format": "uri"},
            },
            "required": [
                "ipd_sharing",
                "ipd_sharing_description",
                "ipd_sharing_info_type_list",
                "ipd_sharing_time_frame",
                "ipd_sharing_access_criteria",
                "ipd_sharing_url",
            ],
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: typing.Union[dict, typing.Any] = request.json
        if data["ipd_sharing"] == "Yes":
            required_fields = [
                "ipd_sharing_description",
                "ipd_sharing_info_type_list",
                "ipd_sharing_time_frame",
                "ipd_sharing_access_criteria",
                "ipd_sharing_url",
            ]

            for field in required_fields:
                if field not in data:
                    return f"Field {field} is required", 400

        study_ = model.Study.query.get(study_id)
        if not is_granted("study_metadata", study_):
            return "Access denied, you can not modify study", 403
        study_.study_ipdsharing.update(request.json)
        model.db.session.commit()
        return study_.study_ipdsharing.to_dict(), 200
