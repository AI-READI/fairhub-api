from flask_restx import Namespace, Resource, fields
from model import Study

api = Namespace("reference", description="study operations", path="/")


study_reference = api.model(
    "StudyReference",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "type": fields.Boolean(required=True),
        "title": fields.String(required=True),
        "citation": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/reference")
class StudyReferenceResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_reference)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_reference_ = study_.study_reference
        return [s.to_dict() for s in study_reference_]
