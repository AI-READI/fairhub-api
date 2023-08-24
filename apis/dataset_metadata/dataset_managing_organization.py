from model import Dataset

from flask_restx import Namespace, Resource, fields


api = Namespace("managing_organization", description="dataset operations", path="/")

managing_organization = api.model(
    "DatasetManagingOrganization",
    {
        "id": fields.String(required=True),
        "name": fields.String(required=True),
        "ror_id": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/managing_organization")
class DatasetManagingOrganizationResource(Resource):
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(managing_organization)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        managing_organization_ = dataset_.dataset_managing_organization
        return [d.to_dict() for d in managing_organization_]
