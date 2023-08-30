from model import Dataset, db, DatasetDescription

from flask_restx import Resource, fields
from flask import request


from apis.dataset_metadata_namespace import api

dataset_description = api.model(
    "DatasetDescription",
    {
        "id": fields.String(required=True),
        "description": fields.String(required=True),
        "description_type": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/description")
class DatasetDescriptionResource(Resource):
    @api.doc("description")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_description)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_description_ = dataset_.dataset_description
        return [d.to_dict() for d in dataset_description_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        dataset_description_ = DatasetDescription.from_data(data_obj, data)
        db.session.add(dataset_description_)
        db.session.commit()
        return dataset_description_.to_dict()

    @api.route(
        "/study/<study_id>/dataset/<dataset_id>/metadata/description/<description_id>"
    )
    class DatasetDescriptionUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, description_id: int):
            dataset_description_ = DatasetDescription.query.get(description_id)
            dataset_description_.update(request.json)
            db.session.commit()
            return dataset_description_.to_dict()
