from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

dataset_record_keys = api.model(
    "DatasetRecordKeys",
    {
        "id": fields.String(required=True),
        "key_type": fields.String(required=False),
        "key_details": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/record-keys")
class DatasetRecordKeysResource(Resource):
    @api.doc("record keys")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_record_keys)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)

        dataset_record_keys_ = dataset_.dataset_record_keys
        return dataset_record_keys_.to_dict()

    @api.doc("update record keys")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_record_keys.update(data)
        model.db.session.commit()
        return dataset_.dataset_record_keys.to_dict(), 201
