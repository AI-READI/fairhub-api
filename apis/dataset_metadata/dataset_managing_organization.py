from model import Dataset, db, DatasetManagingOrganization
from flask import request

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

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        managing_organization_ = DatasetManagingOrganization.from_data(data_obj, data)
        db.session.add(managing_organization_)
        db.session.commit()
        return managing_organization_.to_dict()

    @api.route(
        "/study/<study_id>/dataset/<dataset_id>/metadata/managing_organization/<managing_organization_id>"
    )
    class DatasetManagingOrganizationUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, managing_organization_id: int):
            managing_organization_ = DatasetManagingOrganization.query.get(
                managing_organization_id
            )
            managing_organization_.update(request.json)
            db.session.commit()
            return managing_organization_.to_dict()
