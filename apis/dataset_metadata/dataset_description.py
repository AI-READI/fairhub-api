from model import Dataset

from flask_restx import Namespace, Resource, fields


api = Namespace("description", description="dataset operations", path="/")

dataset_description = api.model(
    "DatasetDescription",
    {
        "id": fields.String(required=True),
        "description": fields.String(required=True),
        "description_type": fields.String(required=True),

    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/description")
class DatasetDescriptionResource(Resource):
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_description)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_description_ = dataset_.dataset_description
        return [d.to_dict() for d in dataset_description_]
