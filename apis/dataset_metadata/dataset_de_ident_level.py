from flask import request
from flask_restx import Resource, fields

import model
from apis.authentication import is_granted
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


@api.route("/study/<study_id>/dataset/<dataset_id>/de-identification-level")
class DatasetDeIdentLevelResource(Resource):
    @api.doc("de_ident_level")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(de_ident_level)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        dataset_ = model.Dataset.query.get(dataset_id)
        de_ident_level_ = dataset_.dataset_de_ident_level
        return de_ident_level_.to_dict()

    @api.doc("update ident level")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_de_ident_level.update(data)
        model.db.session.commit()
        return dataset_.dataset_de_ident_level.to_dict()
