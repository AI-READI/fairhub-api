from model import Study

from flask_restx import Namespace, Resource, fields


api = Namespace("link", description="study operations", path="/")


study_link = api.model(
    "StudyLink",
    {
        "id": fields.String(required=True),
        "url": fields.String(required=True),
        "title": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/link")
class StudyLinkResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_link)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_link_ = study_.study_link
        return [s.to_dict() for s in study_link_]
