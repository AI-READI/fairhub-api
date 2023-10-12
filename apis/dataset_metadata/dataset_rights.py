from typing import Any

from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

dataset_rights = api.model(
    "DatasetRights",
    {
        "id": fields.String(required=True),
        "rights": fields.String(required=True),
        "uri": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_scheme": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/rights")
class DatasetRightsResource(Resource):
    @api.doc("rights")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_rights)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_rights_ = dataset_.dataset_rights
        return [d.to_dict() for d in dataset_rights_]

    def post(self, study_id: int, dataset_id: int):
        data: Any | dict = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        dataset_rights_ = model.DatasetRights.from_data(data_obj, data)
        model.db.session.add(dataset_rights_)
        model.db.session.commit()
        return dataset_rights_.to_dict()

    @api.route("/study/<study_id>/dataset/<dataset_id>/metadata/rights/<rights_id>")
    class DatasetRightsUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, rights_id: int):
            dataset_rights_ = model.DatasetRights.query.get(rights_id)
            dataset_rights_.update(request.json)
            model.db.session.commit()
            return dataset_rights_.to_dict()
