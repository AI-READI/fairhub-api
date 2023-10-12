"""API routes for study design metadata"""
from flask_restx import Resource, fields
from flask import request
from jsonschema import validate, ValidationError
from model import Study, db
from ..authentication import is_granted


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
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "design_allocation": {"type": "string"},
                "study_type": {"type": "string"},
                "design_intervention_model": {"type": "string"},
                "design_intervention_model_description": {"type": "string"},
                "design_primary_purpose": {"type": "string"},
                "design_masking": {"type": "string"},
                "design_masking_description": {"type": "string"},
                "design_who_masked_list": {"type": "array", "items": {"type": "string"}},
                "phase_list": {"type": "array", "items": {"type": "string"}},
                "enrollment_count": {"type": "integer"},
                "enrollment_type": {"type": "string"},
                "number_arms": {"type": "integer"},
                "design_observational_model_list": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "design_time_perspective_list": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "bio_spec_retention": {"type": "string"},
                "bio_spec_description": {"type": "string"},
                "target_duration": {"type": "string"},
                "number_groups_cohorts": {"type": "integer"},
            }
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        study = Study.query.get(study_id)
        # Check user permissions
        if not is_granted("study_metadata", study):
            return "Access denied, you can not delete study", 403

        study_ = Study.query.get(study_id)

        study_.study_design.update(request.json)

        db.session.commit()

        return study_.study_design.to_dict()
