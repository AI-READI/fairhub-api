from model import Dataset

from flask_restx import Namespace, Resource, fields


api = Namespace("description", description="dataset operations", path="/")

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
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_subject)
    def get(self, study_id: int, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_subject_ = dataset_.dataset_subject
        return [d.to_dict() for d in dataset_subject_]
