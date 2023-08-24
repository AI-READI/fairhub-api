from model import Dataset

from flask_restx import Namespace, Resource, fields


api = Namespace("related_item_other", description="dataset operations", path="/")

# dataset_related_item_contributor = api.model(
#     "DatasetRelatedItemContributor",
#     {
#         "id": fields.String(required=True),
#         "type": fields.String(required=True),
#         "relation_type": fields.String(required=True),
#
#     },
# )


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/related_item_other")
class DatasetRelatedItemContributorResource(Resource):
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    # @api.marshal_with(dataset_related_item_contributor)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_related_item_ = dataset_.dataset_related_item
        return [d.to_dict() for d in dataset_related_item_]
