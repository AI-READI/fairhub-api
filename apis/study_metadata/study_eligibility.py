"""API routes for study eligibility metadata"""
from flask import request
from flask_restx import Resource, fields

from apis.study_metadata_namespace import api
from model import Study, db

from ..authentication import is_granted

study_eligibility = api.model(
    "StudyEligibility",
    {
        "id": fields.String(required=True),
        "gender": fields.String(required=True),
        "gender_based": fields.String(required=True),
        "gender_description": fields.String(required=True),
        "minimum_age_value": fields.Integer(required=True),
        "maximum_age_value": fields.Integer(required=True),
        "minimum_age_unit": fields.String(required=True),
        "maximum_age_unit": fields.String(required=True),
        "healthy_volunteers": fields.String(required=True),
        "inclusion_criteria": fields.List(fields.String, required=True),
        "exclusion_criteria": fields.List(fields.String, required=True),
        "study_population": fields.String(required=True),
        "sampling_method": fields.String(required=True),
        "study_type": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/eligibility")
class StudyEligibilityResource(Resource):
    """Study Eligibility Metadata"""

    @api.doc("eligibility")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_eligibility)
    def get(self, study_id: int):
        """Get study eligibility metadata"""
        study_ = Study.query.get(study_id)

        return study_.study_eligibility.to_dict()

    def put(self, study_id: int):
        """Update study eligibility metadata"""
        study_ = Study.query.get(study_id)
        if not is_granted("study_metadata", study_):
            return "Access denied, you can not delete study", 403
        study_.study_eligibility.update(request.json)

        db.session.commit()

        return study_.study_eligibility.to_dict()

    # def post(self, study_id: int):
    #     data = request.json
    #     study_eligibility_ = Study.query.get(study_id)
    #     study_eligibility_ = StudyEligibility.from_data(study_eligibility_, data)
    #     db.session.add(study_eligibility_)
    #     db.session.commit()
    #     return study_eligibility_.to_dict()
