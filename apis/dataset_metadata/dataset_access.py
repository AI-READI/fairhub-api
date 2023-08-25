from model import Dataset, DatasetAccess, db

from flask_restx import Resource, fields
from flask import request
from apis.dataset_metadata_namespace import api


dataset_access = api.model(
    "DatasetAccess",
    {
        "id": fields.String(required=True),
        "type": fields.String(required=True),
        "description": fields.String(required=True),
        "url": fields.String(required=True),
        "url_last_checked": fields.String(required=True),

    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/access")
class DatasetAccessResource(Resource):
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_access)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_access_ = dataset_.dataset_access
        return [d.to_dict() for d in dataset_access_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        dataset_request_keys_ = DatasetAccess.from_data(data_obj, data)
        db.session.add(dataset_request_keys_)
        db.session.commit()
        return dataset_request_keys_.to_dict()

    @api.route("/study/<study_id>/dataset/<dataset_id>/metadata/access/<access_id>")
    class DatasetAccessUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, access_id: int):
            data = request.json
            dataset_access_ = DatasetAccess.query.get(access_id)
            dataset_access_.update(request.json)
            db.session.commit()
            return dataset_access_.to_dict()
