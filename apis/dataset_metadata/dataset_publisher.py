from typing import Any, Union

from flask import request
from flask_restx import Resource

import model
from apis.dataset_metadata_namespace import api

# dataset_publisher = api.model(
#     "DatasetPublisher",
#     {
#     },
# )


@api.route("/study/<study_id>/dataset/<dataset_id>/publisher")
class DatasetFunderResource(Resource):
    @api.doc("funder")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_publisher)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_other_ = dataset_.dataset_other
        return [d.to_dict() for d in dataset_other_]

    def post(self, study_id: int, dataset_id: int):
        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        dataset_other_ = model.DatasetOther.from_data(data_obj, data)
        model.db.session.add(dataset_other_)
        model.db.session.commit()
        return dataset_other_.to_dict()


