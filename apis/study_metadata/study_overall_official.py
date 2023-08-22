from flask_restx import Namespace, Resource, fields
from model import Study

api = Namespace("overall_official", description="study operations", path="/")


study_overall_official = api.model(
    "StudyOverallOfficial",
    {
        "id": fields.String(required=True),
        "first_name": fields.String(required=True),
        "last_name": fields.String(required=True),
        "affiliation": fields.String(required=True),
        "role": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/overall_official")
class StudyOverallOfficialResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_overall_official)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_overall_official_ = study_.study_overall_official
        return [s.to_dict() for s in study_overall_official_]


