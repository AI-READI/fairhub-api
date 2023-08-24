from model import Dataset

from flask_restx import Namespace, Resource, fields


api = Namespace("dataset_rights", description="dataset operations", path="/")

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
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_rights)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_rights_ = dataset_.dataset_rights
        return [d.to_dict() for d in dataset_rights_]
