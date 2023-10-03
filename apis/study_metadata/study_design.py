"""API routes for study design metadata"""
from flask_restx import Resource, fields
from flask import request
from model import Study, db


from apis.study_metadata_namespace import api

study_design = api.model(
    "StudyDesign",
    {
        "id": fields.String(required=True),
        "design_allocation": fields.String(required=True),
        "study_type": fields.String(required=True),
        "design_intervention_model": fields.String(required=True),
        "design_intervention_model_description": fields.String(required=True),
        "design_primary_purpose": fields.String(required=True),
        "design_masking": fields.String(required=True),
        "design_masking_description": fields.String(required=True),
        "design_who_masked_list": fields.List(fields.String, required=True),
        "phase_list": fields.List(fields.String, required=True),
        "enrollment_count": fields.Integer(required=True),
        "enrollment_type": fields.String(required=True),
        "number_arms": fields.Integer(required=True),
        "design_observational_model_list": fields.List(fields.String, required=True),
        "design_time_perspective_list": fields.List(fields.String, required=True),
        "bio_spec_retention": fields.String(required=True),
        "bio_spec_description": fields.String(required=True),
        "target_duration": fields.String(required=True),
        "number_groups_cohorts": fields.Integer(required=True),
    },
)


@api.route("/study/<study_id>/metadata/design")
class StudyDesignResource(Resource):
    """Study Design Metadata"""

    @api.doc("design")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(study_design)
    def get(self, study_id: int):
        """Get study design metadata"""
        study_ = Study.query.get(study_id)

        study_design_ = study_.study_design

        return study_design_.to_dict()

    def put(self, study_id: int):
        """Update study design metadata"""
        study_ = Study.query.get(study_id)

        study_.study_design.update(request.json)

        db.session.commit()

        return study_.study_design.to_dict()
