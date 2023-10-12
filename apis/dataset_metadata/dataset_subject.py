from typing import Any

from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

dataset_subject = api.model(
    "DatasetSubject",
    {
        "id": fields.String(required=True),
        "subject": fields.String(required=True),
        "scheme": fields.String(required=True),
        "scheme_uri": fields.String(required=True),
        "value_uri": fields.String(required=True),
        "classification_code": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/subject")
class DatasetSubjectResource(Resource):
    @api.doc("subject")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_subject)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_subject_ = dataset_.dataset_subject
        return [d.to_dict() for d in dataset_subject_]

    def post(self, study_id: int, dataset_id: int):
        data: Any | dict = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        dataset_subject_ = model.DatasetSubject.from_data(data_obj, data)
        model.db.session.add(dataset_subject_)
        model.db.session.commit()
        return dataset_subject_.to_dict()

    @api.route("/study/<study_id>/dataset/<dataset_id>/metadata/subject/<subject_id>")
    class DatasetSubjectUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, subject_id: int):
            dataset_subject_ = model.DatasetSubject.query.get(subject_id)
            dataset_subject_.update(request.json)
            model.db.session.commit()
            return dataset_subject_.to_dict()
