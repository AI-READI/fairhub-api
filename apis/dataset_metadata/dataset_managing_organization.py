import typing
from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

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
    @api.doc("managing_organization")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(managing_organization)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        managing_organization_ = dataset_.dataset_managing_organization
        return [d.to_dict() for d in managing_organization_]

    def put(self, study_id: int, dataset_id: int):
        data: typing.Union[dict, typing.Any] = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        managing_organization_ = dataset_.dataset_managing_organization.update(data)
        model.db.session.commit()
        return managing_organization_.to_dict()
