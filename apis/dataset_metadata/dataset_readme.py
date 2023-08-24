from model import Dataset

from flask_restx import Namespace, Resource, fields


api = Namespace("readme", description="dataset operations", path="/")

dataset_readme = api.model(
    "DatasetReadme",
    {
        "id": fields.String(required=True),
        "content": fields.Boolean(required=True)

    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/readme")
class DatasetDateResource(Resource):
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_readme)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_readme_ = dataset_.dataset_readme
        return [d.to_dict() for d in dataset_readme_]
