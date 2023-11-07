"""API for dataset consent metadata"""
from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_consent = api.model(
    "DatasetConsent",
    {
        "id": fields.String(required=True),
        "type": fields.String(required=True),
        "noncommercial": fields.Boolean(required=True),
        "geog_restrict": fields.Boolean(required=True),
        "research_type": fields.Boolean(required=True),
        "genetic_only": fields.Boolean(required=True),
        "no_methods": fields.Boolean(required=True),
        "details": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/consent")
class DatasetConsentResource(Resource):
    """Dataset Consent Resource"""

    @api.doc("consent")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_consent)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset consent"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_consent_ = dataset_.dataset_consent
        return dataset_consent_.to_dict()

    @api.doc("update consent")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        """Update dataset consent"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "type": {"type": "string", "minLength": 1},
                "details": {
                    "type": "string",
                },
                "genetic_only": {"type": "boolean"},
                "geog_restrict": {"type": "boolean"},
                "no_methods": {"type": "boolean"},
                "noncommercial": {"type": "boolean"},
                "research_type": {"type": "boolean"},
            },
            "required": [
                "type",
                "details",
                "genetic_only",
                "geog_restrict",
                "no_methods",
                "noncommercial",
                "research_type",
            ],
        }

        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_consent.update(data)
        model.db.session.commit()
        return dataset_.dataset_consent.to_dict()
