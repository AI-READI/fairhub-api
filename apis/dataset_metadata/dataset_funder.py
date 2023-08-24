from model import Dataset

from flask_restx import Namespace, Resource, fields


api = Namespace("description", description="dataset operations", path="/")

dataset_funder = api.model(
    "DatasetFunder",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_type": fields.String(required=True),
        "identifier_scheme_uri": fields.String(required=True),
        "award_number": fields.String(required=True),
        "award_uri": fields.String(required=True),
        "award_title": fields.String(required=True),

    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/funder")
class DatasetFunderResource(Resource):
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_funder)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_funder_ = dataset_.dataset_funder
        return [d.to_dict() for d in dataset_funder_]
