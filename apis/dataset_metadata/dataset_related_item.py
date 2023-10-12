from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

dataset_related_item = api.model(
    "DatasetRelatedItem",
    {
        "id": fields.String(required=True),
        "type": fields.String(required=True),
        "relation_type": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/related_item")
class DatasetRelatedItemResource(Resource):
    @api.doc("related_item")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_related_item)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_related_item_ = dataset_.dataset_related_item
        return [d.to_dict() for d in dataset_related_item_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        dataset_related_item_ = model.DatasetRelatedItem.from_data(data_obj, data)
        model.db.session.add(dataset_related_item_)
        model.db.session.commit()
        return dataset_related_item_.to_dict()

    @api.route(
        "/study/<study_id>/dataset/<dataset_id>/metadata/related_item/<related_item_id>"
    )
    class DatasetRelatedItemUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, related_item_id: int):
            data = request.json
            dataset_related_item_ = model.DatasetRelatedItem.query.get(related_item_id)
            dataset_related_item_.update(data)
            model.db.session.commit()
            return dataset_related_item_.to_dict()
