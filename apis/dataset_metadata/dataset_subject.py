from model import Dataset, DatasetSubject, db

from flask_restx import Namespace, Resource, fields
from flask import jsonify, request

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
        dataset_ = Dataset.query.get(dataset_id)
        dataset_subject_ = dataset_.dataset_subject
        return [d.to_dict() for d in dataset_subject_]

    def post(self, study_id: int, dataset_id: int):
        data = request.json
        data_obj = Dataset.query.get(dataset_id)
        dataset_subject_ = DatasetSubject.from_data(data_obj, data)
        db.session.add(dataset_subject_)
        db.session.commit()
        return dataset_subject_.to_dict()

    @api.route("/study/<study_id>/dataset/<dataset_id>/metadata/subject/<subject_id>")
    class DatasetSubjectUpdate(Resource):
        def put(self, study_id: int, dataset_id: int, subject_id: int):
            dataset_subject_ = DatasetSubject.query.get(subject_id)
            dataset_subject_.update(request.json)
            db.session.commit()
            return dataset_subject_.to_dict()
