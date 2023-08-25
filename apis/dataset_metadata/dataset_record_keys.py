from model import Dataset, DatasetRecordKeys, db

from flask_restx import Namespace, Resource, fields
from flask import jsonify, request
from apis.dataset_metadata_namespace import api

dataset_record_keys = api.model(
    "DatasetRecordKeys",
    {
        "id": fields.String(required=True),
        "key_type": fields.String(required=True),
        "key_details": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/record_keys")
class DatasetRecordKeysResource(Resource):
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_record_keys)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_record_keys_ = dataset_.dataset_record_keys
        return [d.to_dict() for d in dataset_record_keys_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        dataset_record_keys_ = DatasetRecordKeys.from_data(data_obj, data)
        db.session.add(dataset_record_keys_)
        db.session.commit()
        return dataset_record_keys_.to_dict()

    @api.route(
        "/study/<study_id>/dataset/<dataset_id>/metadata/record_keys/<record_key_id>"
    )
    class DatasetRecordKeysUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, record_key_id: int):
            data = request.json
            dataset_record_keys_ = DatasetRecordKeys.query.get(record_key_id)
            dataset_record_keys_.update(request.json)
            db.session.commit()
            return dataset_record_keys_.to_dict()
