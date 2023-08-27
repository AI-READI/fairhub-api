from model import Dataset, db, DatasetDate

from flask_restx import Resource, fields
from flask import request
from apis.dataset_metadata_namespace import api


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
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_date)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_date_ = dataset_.dataset_date
        return [d.to_dict() for d in dataset_date_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        dataset_date_ = DatasetDate.from_data(data_obj, data)
        db.session.add(dataset_date_)
        db.session.commit()
        return dataset_date_.to_dict()

    @api.route("/study/<study_id>/dataset/<dataset_id>/metadata/date/<date_id>")
    class DatasetDateUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, date_id: int):
            dataset_date_ = DatasetDate.query.get(date_id)
            dataset_date_.update(request.json)
            db.session.commit()
            return dataset_date_.to_dict()
