from flask import request
from flask_restx import Resource, fields

from apis.dataset_metadata_namespace import api
from model import Dataset, DatasetRights, db

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
    @api.doc("rights")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_rights)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_rights_ = dataset_.dataset_rights
        return [d.to_dict() for d in dataset_rights_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        dataset_rights_ = DatasetRights.from_data(data_obj, data)
        db.session.add(dataset_rights_)
        db.session.commit()
        return dataset_rights_.to_dict()

    @api.route("/study/<study_id>/dataset/<dataset_id>/metadata/rights/<rights_id>")
    class DatasetRightsUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, rights_id: int):
            dataset_rights_ = DatasetRights.query.get(rights_id)
            dataset_rights_.update(request.json)
            db.session.commit()
            return dataset_rights_.to_dict()
