from model import Dataset

from flask_restx import Namespace, Resource, fields


api = Namespace("title", description="dataset operations", path="/")

dataset_title = api.model(
    "StudyContact",
    {
        "id": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "affiliation": fields.String(required=True),
        "role": fields.String(required=True),
        "phone": fields.String(required=True),
        "phone_ext": fields.String(required=True),
        "email_address": fields.String(required=True),
        "central_contact": fields.Boolean(required=True),
    },
)


@api.route("/study/<study_id>/metadata/contact")
class StudyContactResource(Resource):
    @api.doc("dataset")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_title)
    def get(self, dataset_id: int):
        dataset_ = Dataset.query.get(dataset_id)
        dataset_title_ = dataset_.dataset_title
        return [d.to_dict() for d in dataset_title_]
