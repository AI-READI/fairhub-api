from flask import request
from flask_restx import Resource, fields

from apis.dataset_metadata_namespace import api
from model import Dataset, db

dataset_readme = api.model(
    "DatasetReadme",
    {"id": fields.String(required=True), "content": fields.String(required=True)},
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/readme")
class DatasetReadmeResource(Resource):
    @api.doc("readme")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_readme)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_readme_ = dataset_.dataset_readme
        return [d.to_dict() for d in dataset_readme_]

    def put(self, study_id: int, dataset_id: int):
        data = request.json
        dataset_ = Dataset.query.get(dataset_id)
        dataset_readme_ = dataset_.dataset_readme.update(data)
        db.session.commit()
        return dataset_readme_.to_dict()
