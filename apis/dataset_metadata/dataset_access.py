from flask import request
from flask_restx import Resource, fields

import model
from apis.authentication import is_granted
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


@api.route("/study/<study_id>/dataset/<dataset_id>/access")
class DatasetAccessResource(Resource):
    @api.doc("access")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_access)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_access_ = dataset_.dataset_access
        return dataset_access_.to_dict()

    @api.doc("update access")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_access.update(request.json)
        model.db.session.commit()
        return dataset_.dataset_access.to_dict()
