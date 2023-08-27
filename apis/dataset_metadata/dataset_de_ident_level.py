from model import Dataset, DatasetDeIdentLevel, db

from flask_restx import Resource, fields
from flask import request

from apis.dataset_metadata_namespace import api

de_ident_level = api.model(
    "DatasetDeIdentLevel",
    {
        "id": fields.String(required=True),
        "type": fields.String(required=True),
        "direct": fields.Boolean(required=True),
        "hipaa": fields.Boolean(required=True),
        "dates": fields.Boolean(required=True),
        "nonarr": fields.Boolean(required=True),
        "k_anon": fields.Boolean(required=True),
        "details": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/de_ident_level")
class DatasetDeIdentLevelResource(Resource):
    @api.doc("de_ident_level")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(de_ident_level)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        de_ident_level_ = dataset_.dataset_de_ident_level
        return [d.to_dict() for d in de_ident_level_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        de_ident_level_ = DatasetDeIdentLevel.from_data(data_obj, data)
        db.session.add(de_ident_level_)
        db.session.commit()
        return de_ident_level_.to_dict()

    @api.route(
        "/study/<study_id>/dataset/<dataset_id>/metadata/de_ident_level/<de_ident_level_id>"
    )
    class DatasetDatasetDeIdentLevelUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, de_ident_level_id: int):
            de_ident_level_ = DatasetDeIdentLevel.query.get(de_ident_level_id)
            de_ident_level_.update(request.json)
            db.session.commit()
            return de_ident_level_.to_dict()
