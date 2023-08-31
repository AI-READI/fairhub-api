from model import Dataset, DatasetTitle, db

from flask_restx import Namespace, Resource, fields
from flask import jsonify, request


from apis.dataset_metadata_namespace import api

dataset_title = api.model(
    "DatasetTitle",
    {
        "id": fields.String(required=True),
        "title": fields.String(required=True),
        "type": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/title")
class DatasetTitleResource(Resource):
    @api.doc("title")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_title)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_title_ = dataset_.dataset_title
        return [d.to_dict() for d in dataset_title_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        dataset_title_ = DatasetTitle.from_data(data_obj, data)
        db.session.add(dataset_title_)
        db.session.commit()
        return dataset_title_.to_dict()

    @api.route("/study/<study_id>/dataset/<dataset_id>/metadata/title/<title_id>")
    class DatasetTitleUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, title_id: int):
            dataset_title_ = DatasetTitle.query.get(title_id)
            dataset_title_.update(request.json)
            db.session.commit()
            return dataset_title_.to_dict()