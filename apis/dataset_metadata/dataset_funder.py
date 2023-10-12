from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

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
    @api.doc("funder")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_funder)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_funder_ = dataset_.dataset_funder
        return [d.to_dict() for d in dataset_funder_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        dataset_funder_ = model.DatasetFunder.from_data(data_obj, data)
        model.db.session.add(dataset_funder_)
        model.db.session.commit()
        return dataset_funder_.to_dict()


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/funder/<funder_id>")
class DatasetFunderUpdate(Resource):
    def put(self, study_id: int, dataset_id: int, funder_id: int):
        dataset_funder_ = model.DatasetFunder.query.get(funder_id)
        dataset_funder_.update(request.json)
        model.db.session.commit()
        return dataset_funder_.to_dict()
