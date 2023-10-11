from flask import request
from flask_restx import Resource, fields

from apis.dataset_metadata_namespace import api
from model import Dataset, DatasetDate, db

dataset_date = api.model(
    "DatasetDate",
    {
        "id": fields.String(required=True),
        "date": fields.String(required=True),
        "date_type": fields.String(required=True),
        "data_information": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/date")
class DatasetDateResource(Resource):
    @api.doc("date")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_date)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_date_ = dataset_.dataset_date
        return [d.to_dict() for d in dataset_date_]

    def put(self, study_id: int, dataset_id: int):
        data = request.json
        dataset_ = Dataset.query.get(dataset_id)
        dataset_date_ = dataset_.dataset_date.update(data)
        db.session.commit()
        return dataset_date_.to_dict()
