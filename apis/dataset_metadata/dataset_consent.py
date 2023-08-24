from model import Dataset, DatasetConsent, db

from flask_restx import Namespace, Resource, fields
from flask import jsonify, request


api = Namespace("consent", description="dataset operations", path="/")

dataset_consent = api.model(
    "DatasetConsent",
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


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/consent")
class DatasetConsentResource(Resource):
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_consent)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_consent_ = dataset_.dataset_consent
        return [d.to_dict() for d in dataset_consent_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        dataset_consent_ = DatasetConsent.from_data(data_obj, data)
        db.session.add(dataset_consent_)
        db.session.commit()
        return jsonify(dataset_consent_.to_dict())