from model import Dataset, db, DatasetIdentifier
from flask_restx import Resource, fields
from flask import request

from apis.dataset_metadata_namespace import api

dataset_identifier = api.model(
    "DatasetIdentifier",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_type": fields.String(required=True),
        "alternate": fields.Boolean(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/identifier")
class DatasetIdentifierResource(Resource):
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_identifier)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_identifier_ = dataset_.dataset_identifier
        return [d.to_dict() for d in dataset_identifier_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        dataset_identifier_ = DatasetIdentifier.from_data(data_obj, data)
        db.session.add(dataset_identifier_)
        db.session.commit()
        return dataset_identifier_.to_dict()

    @api.route(
        "/study/<study_id>/dataset/<dataset_id>/metadata/identifier/<identifier_id>"
    )
    class DatasetIdentifierUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, identifier_id: int):
            dataset_identifier_ = DatasetIdentifier.query.get(identifier_id)
            dataset_identifier_.update(request.json)
            db.session.commit()
            return dataset_identifier_.to_dict()
