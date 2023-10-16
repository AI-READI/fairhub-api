from flask_restx import Resource

import model
from apis.dataset_metadata_namespace import api

# dataset_related_item_contributor = api.model(
#     "DatasetRelatedItemContributor",
#     {
#         "id": fields.String(required=True),
#         "type": fields.String(required=True),
#         "relation_type": fields.String(required=True),
#
#     },
# )


@api.route("/study/<study_id>/dataset/<dataset_id>/related_item_other")
class DatasetRelatedItemContributorResource(Resource):
    @api.doc("related_item_other")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    # @api.marshal_with(dataset_related_item_contributor)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_related_item_ = dataset_.dataset_related_item
        return [d.to_dict() for d in dataset_related_item_]
