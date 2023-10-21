from flask import request
from flask_restx import Resource, fields

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_readme = api.model(
    "DatasetReadme",
    {"id": fields.String(required=True), "content": fields.String(required=True)},
)


@api.route("/study/<study_id>/dataset/<dataset_id>/readme")
class DatasetReadmeResource(Resource):
    @api.doc("readme")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_readme)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_readme_ = dataset_.dataset_readme
        return [d.to_dict() for d in dataset_readme_]

    def put(self, study_id: int, dataset_id: int):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_readme_ = dataset_.dataset_readme.update(data)
        model.db.session.commit()
        return dataset_readme_.to_dict()
