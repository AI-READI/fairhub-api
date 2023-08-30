from model import Dataset, DatasetConsent, db

from flask_restx import Resource, fields
from flask import request
from apis.dataset_metadata_namespace import api


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
    @api.doc("consent")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_consent)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_consent_ = dataset_.dataset_consent
        return [d.to_dict() for d in dataset_consent_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                dataset_consent_ = DatasetConsent.query.get(i["id"])
                if dataset_consent_ == None:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_consent_.update(i)
                list_of_elements.append(dataset_consent_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_consent_ = DatasetConsent.from_data(data_obj, i)
                db.session.add(dataset_consent_)
                list_of_elements.append(dataset_consent_.to_dict())
        db.session.commit()
        return list_of_elements

    @api.route("/study/<study_id>/dataset/<dataset_id>/metadata/consent/<consent_id>")
    class DatasetAccessUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, consent_id: int):
            dataset_consent_ = DatasetConsent.query.get(consent_id)
            dataset_consent_.update(request.json)
            db.session.commit()
            return dataset_consent_.to_dict()
