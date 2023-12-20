"""API endpoints for other dataset metadata"""
from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_other = api.model(
    "DatasetOther",
    {
        "id": fields.String(required=True),
        "language": fields.String(required=True),
        "managing_organization_name": fields.String(required=True),
        "managing_organization_ror_id": fields.String(required=True),
        "size": fields.List(fields.String, required=True),
        "standards_followed": fields.String(required=True),
        "acknowledgement": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/other")
class DatasetOtherResource(Resource):
    """Dataset Other Resource"""

    @api.doc("other")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_other)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset other metadata"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_other_ = dataset_.dataset_other
        return dataset_other_.to_dict(), 200

    @api.doc("other update")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_other)
    def put(self, study_id: int, dataset_id: int):
        """Update dataset other metadata"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "acknowledgement": {"type": "string"},
                "language": {"type": "string"},
                "resource_type": {"type": "string"},
                "size": {
                    "type": "array",
                    "items": {"type": "string"},
                    "uniqueItems": True,
                },
                "standards_followed": {"type": "string"},
            },
            "required": [
                "acknowledgement",
                "language",
                "resource_type",
                "size",
                "standards_followed",
            ],
        }

        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_other.update(data)
        model.db.session.commit()
        return dataset_.dataset_other.to_dict(), 200


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
        dataset_other_ = dataset_.dataset_other
        return dataset_other_.to_dict(), 200

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
                "publisher": {"type": "string", "minLength": 1},
                "managing_organization_name": {"type": "string", "minLength": 1},
                "managing_organization_ror_id": {
                    "type": "string",
                },
            },
            "required": [
                "publisher",
                "managing_organization_name",
                "managing_organization_ror_id",
            ],
        }

        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_other.update(data)
        model.db.session.commit()
        return dataset_.dataset_other.to_dict(), 200
