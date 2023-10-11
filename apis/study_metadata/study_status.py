"""API routes for study status metadata"""
from flask import request
from flask_restx import Resource, fields

from apis.study_metadata_namespace import api
from model import Study, db

from ..authentication import is_granted

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
    """Study Status Metadata"""

    @api.doc("status")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_status)
    def get(self, study_id: int):
        """Get study status metadata"""
        study_ = Study.query.get(study_id)

        study_status_ = study_.study_status

        return study_status_.to_dict()

    def put(self, study_id: int):
        """Update study status metadata"""
        study_obj = Study.query.get(study_id)
        if not is_granted("study_metadata", study_obj):
            return "Access denied, you can not delete study", 403
        study = Study.query.get(study_id)

        study.study_status.update(request.json)

        db.session.commit()

        return study.study_status.to_dict()
