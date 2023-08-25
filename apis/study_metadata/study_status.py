from flask_restx import Namespace, Resource, fields
from model import Study

from apis.study_metadata_namespace import api


study_status = api.model(
    "StudyStatus",
    {
        "id": fields.String(required=True),
        "overall_status": fields.String(required=True),
        "why_stopped": fields.String(required=True),
        "start_date": fields.String(required=True),
        "start_date_type": fields.String(required=True),
        "completion_date": fields.String(required=True),
        "completion_date_type": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/status")
class StudyStatusResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_status)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_status_ = study_.study_status
        return [s.to_dict() for s in study_status_]
