from model import Dataset, db, DatasetOther
from flask import request

from flask_restx import Namespace, Resource, fields

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
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_other)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_other_ = dataset_.dataset_other
        return [d.to_dict() for d in dataset_other_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        dataset_other_ = DatasetOther.from_data(data_obj, data)
        db.session.add(dataset_other_)
        db.session.commit()
        return dataset_other_.to_dict()

    @api.route("/study/<study_id>/dataset/<dataset_id>/metadata/other/<other_id>")
    class DatasetOtherUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, other_id: int):
            dataset_other_ = DatasetOther.query.get(other_id)
            dataset_other_.update(request.json)
            db.session.commit()
            return dataset_other_.to_dict()
