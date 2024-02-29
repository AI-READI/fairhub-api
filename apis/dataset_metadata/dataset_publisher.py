"""API endpoints for other dataset metadata"""

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/publisher")
class DatasetPublisherResource(Resource):
    """Dataset Publisher Resource"""

    @api.doc("publisher")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_publisher)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset publisher metadata"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_publisher_ = dataset_.dataset_publisher
        return dataset_publisher_.to_dict(), 200

    @api.doc("update publisher")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        """Update dataset publisher metadata"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "publisher_name": {"type": "string", "minLength": 1},
                "publisher_identifier": {"type": "string", "minLength": 1},
                "publisher_identifier_scheme": {"type": "string", "minLength": 1},
                "managing_organization_name": {"type": "string", "minLength": 1},
                "publisher_identifier_scheme_uri": {"type": "string", "minLength": 1},
                "managing_organization_ror_id": {
                    "type": "string",
                },

            },
            "required": [
                "publisher_name",
                "publisher_identifier",
                "publisher_identifier_scheme",
                "managing_organization_name",
                "publisher_identifier_scheme_uri",
                "managing_organization_ror_id",
            ],
        }

        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_publisher.update(data)
        dataset_.dataset_other.update(data)

        model.db.session.commit()
        return dataset_.dataset_publisher.to_dict(), 200
