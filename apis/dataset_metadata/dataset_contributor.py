from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

dataset_consent = api.model(
    "DatasetContributor",
    {
        "id": fields.String(required=True),
        "type": fields.String(required=True),
        "noncommercial": fields.Boolean(required=True),
        "geog_restrict": fields.Boolean(required=True),
        "research_type": fields.Boolean(required=True),
        "genetic_only": fields.Boolean(required=True),
        "no_methods": fields.Boolean(required=True),
        "details": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/contributor")
class DatasetContributorResource(Resource):
    @api.doc("consent")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_consent)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_contributor_ = dataset_.dataset_contributor
        return [d.to_dict() for d in dataset_contributor_]

    def put(self, study_id: int, dataset_id: int):
        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_contributor_ = dataset_.dataset_contributor.update(data)
        model.db.session.commit()
        return dataset_contributor_.to_dict()
