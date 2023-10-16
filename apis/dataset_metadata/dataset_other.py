from typing import Union, Any

from flask import request
from flask_restx import Resource, fields

import model
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


@api.route("/study/<study_id>/dataset/<dataset_id>/other")
class DatasetOtherResource(Resource):
    @api.doc("other")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_other)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_other_ = dataset_.dataset_other
        return dataset_other_.to_dict()

    def put(self, study_id: int, dataset_id: int):
        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_other.update(data)
        model.db.session.commit()
        return dataset_.dataset_other.to_dict()


@api.route("/study/<study_id>/dataset/<dataset_id>/publisher")
class DatasetPublisherResource(Resource):
    @api.doc("publisher")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_publisher)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_other_ = dataset_.dataset_other
        return dataset_other_.to_dict()

    @api.doc("update publisher")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_other.update(data)
        model.db.session.commit()
        return dataset_.dataset_other.to_dict()
