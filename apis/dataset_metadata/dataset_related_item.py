from model import Dataset, DatasetRelatedItem, db

from flask_restx import Namespace, Resource, fields
from flask import jsonify, request


api = Namespace("related_item", description="dataset operations", path="/")

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
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_related_item)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_related_item_ = dataset_.dataset_related_item
        return [d.to_dict() for d in dataset_related_item_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        dataset_related_item_ = DatasetRelatedItem.from_data(data_obj, data)
        db.session.add(dataset_related_item_)
        db.session.commit()
        return dataset_related_item_.to_dict()

    @api.route(
        "/study/<study_id>/dataset/<dataset_id>/metadata/related_item/<related_item_id>"
    )
    class DatasetRelatedItemUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, related_item_id: int):
            data = request.json
            dataset_related_item_ = DatasetRelatedItem.query.get(related_item_id)
            dataset_related_item_.update(request.json)
            db.session.commit()
            return dataset_related_item_.to_dict()
