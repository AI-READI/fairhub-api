"""API endpoints for other dataset metadata"""

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_managing_organization = api.model(
    "DatasetManagingOrganization",
    {
        "managing_organization_name": fields.String(required=True),
        "managing_organization_ror_id": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/managing-organization")
class DatasetManagingOrganization(Resource):
    """Dataset Publisher Resource"""

    @api.doc("publisher")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_managing_organization)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset publisher metadata"""
        dataset_ = model.Dataset.query.get(dataset_id)
        managing_organization_ = dataset_.dataset_other
        return managing_organization_.to_dict(), 200

    @api.doc("update organization")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_managing_organization)
    def put(self, study_id: int, dataset_id: int):
        """Update dataset managing organization metadata"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "managing_organization_name": {"type": "string", "minLength": 1},
                "managing_organization_ror_id": {
                    "type": "string",
                },
            },
            "required": ["managing_organization_name", "managing_organization_ror_id"],
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
