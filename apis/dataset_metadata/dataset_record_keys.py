"""API endpoints for dataset record keys"""
from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_record_keys = api.model(
    "DatasetRecordKeys",
    {
        "id": fields.String(required=True),
        "key_type": fields.String(required=False),
        "key_details": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/record-keys")
class DatasetRecordKeysResource(Resource):
    """Dataset Record Keys Resource"""

    @api.doc("record keys")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_record_keys)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset record keys"""
        dataset_ = model.Dataset.query.get(dataset_id)

        dataset_record_keys_ = dataset_.dataset_record_keys
        return dataset_record_keys_.to_dict(), 200

    @api.doc("update record keys")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        """Update dataset record keys"""
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
            },
            "required": [
                "type",
                "details",
            ],
        }

        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_record_keys.update(data)
        model.db.session.commit()
        return dataset_.dataset_record_keys.to_dict(), 200
