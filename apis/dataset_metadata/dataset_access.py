from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

dataset_access = api.model(
    "DatasetAccess",
    {
        "id": fields.String(required=True),
        "type": fields.String(required=True),
        "description": fields.String(required=True),
        "url": fields.String(required=True),
        "url_last_checked": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/access")
class DatasetAccessResource(Resource):
    @api.doc("access")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_access)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_access_ = dataset_.dataset_access
        return [d.to_dict() for d in dataset_access_]

    def put(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_access_ = dataset_.dataset_access.update(request.json)
        model.db.session.commit()
        return dataset_access_.to_dict()
