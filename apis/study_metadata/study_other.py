from flask_restx import Namespace, Resource, fields
from model import Study

api = Namespace("other", description="study operations", path="/")


study_other = api.model(
    "StudyOther",
    {
        "id": fields.String(required=True),
        "oversight_has_dmc": fields.String(required=True),
        "conditions": fields.String(required=True),
        "keywords": fields.String(required=True),
        "size": fields.Integer(required=True)
    },
)


@api.route("/study/<study_id>/metadata/other")
class StudyOtherResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_other)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_other_ = study_.study_other
        return [s.to_dict() for s in study_other_]


