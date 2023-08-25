from model import Dataset, db, DatasetReadme
from flask import request

from flask_restx import Namespace, Resource, fields

from apis.dataset_metadata_namespace import api

dataset_readme = api.model(
    "DatasetReadme",
    {
        "id": fields.String(required=True),
        "content": fields.String(required=True)

    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/readme")
class DatasetReadmeResource(Resource):
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_readme)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_readme_ = dataset_.dataset_readme
        return [d.to_dict() for d in dataset_readme_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        dataset_readme_ = DatasetReadme.from_data(data_obj, data)
        db.session.add(dataset_readme_)
        db.session.commit()
        return dataset_readme_.to_dict()

    @api.route("/study/<study_id>/dataset/<dataset_id>/metadata/readme/<readme_id>")
    class DatasetReadmeUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, readme_id: int):
            dataset_readme_ = DatasetReadme.query.get(readme_id)
            dataset_readme_.update(request.json)
            db.session.commit()
            return dataset_readme_.to_dict()
