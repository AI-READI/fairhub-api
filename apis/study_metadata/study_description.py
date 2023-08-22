from model import Study

from flask_restx import Namespace, Resource, fields


api = Namespace("description", description="study operations", path="/")


study_description = api.model(
    "StudyDescription",
    {
        "id": fields.String(required=True),
        "brief_summary": fields.String(required=True),
        "detailed_description": fields.String(required=True),

    },
)


@api.route("/study/<study_id>/metadata/description")
class StudyDescriptionResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_description)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_description_ = study_.study_description
        return [s.to_dict() for s in study_description_]


