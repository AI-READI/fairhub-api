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
            "required": ["study_type"],
            "properties": {
                "design_allocation": {"type": "string", "minLength": 1},
                "study_type": {
                    "type": "string",
                    "oneOf": [
                        {
                            "enum": [
                                "Interventional",
                                "Observational",
                                "Observational Patient Registry",
                                "Expanded Access",
                            ]
                        }
                    ],
                },
                "design_intervention_model": {
                    "type": "string",
                    "oneOf": [
                        {
                            "enum": [
                                "Treatment",
                                "Prevention",
                                "Diagnostic",
                                "Supportive Care",
                                "Screening",
                                "Health Services Research",
                                "Basic Science",
                                "Device Feasibility",
                            ]
                        }
                    ],
                },
                "design_intervention_model_description": {
                    "type": "string",
                    "minLength": 1,
                },
                "design_primary_purpose": {
                    "type": "string",
                    "oneOf": [
                        {
                            "enum": [
                                "Single Group Assignment",
                                "Parallel Assignment",
                                "Crossover Assignment",
                                "Factorial Assignment",
                                "Sequential Assignment",
                            ]
                        }
                    ],
                },
                "design_masking": {
                    "type": "string",
                    "oneOf": [
                        {
                            "enum": [
                                "None (open label)",
                                "Blinded (no details)" "Single",
                                "Double",
                                "Triple",
                                "Quadruple",
                                "N/A",
                            ]
                        }
                    ],
                },
                "design_masking_description": {"type": "string", "minLength": 1},
                "design_who_masked_list": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "oneOf": [
                            {
                                "enum": [
                                    "Participant",
                                    "Care Provider",
                                    "Investigator",
                                    "Outcomes Assessor",
                                ]
                            },
                        ],
                    },
                    "minItems": 1,
                    "uniqueItems": True,
                },
                "phase_list": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "oneOf": [
                            {
                                "enum": [
                                    "N/A",
                                    "Early Phase 1",
                                    "Phase 1",
                                    "Phase 1/2",
                                    "Phase 2",
                                    "Phase 2/3",
                                    "Phase 3",
                                    "Phase 4",
                                ]
                            }
                        ],
                    },
                    "minItems": 1,
                    "uniqueItems": True,
                },
                "enrollment_count": {"type": "integer"},
                "enrollment_type": {"type": "string", "minLength": 1},
                "number_arms": {"type": "integer"},
                "design_observational_model_list": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "oneOf": [
                            {
                                "enum": [
                                    "Cohort",
                                    "Case-Control",
                                    "Case-Only",
                                    "Case-Crossover",
                                    "Ecologic or Community Study",
                                    "Family-Based",
                                    "Other",
                                ]
                            }
                        ],
                    },
                    "minItems": 1,
                    "uniqueItems": True,
                },
                "design_time_perspective_list": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "oneOf": [
                            {
                                "enum": [
                                    "Retrospective",
                                    "Prospective",
                                    "Cross-sectional",
                                    "Other",
                                ]
                            }
                        ],
                    },
                    "minItems": 1,
                    "uniqueItems": True,
                },
                "bio_spec_retention": {
                    "type": "string",
                    "oneOf": [
                        {
                            "enum": [
                                "None Retained",
                                "Samples With DNA",
                                "Samples Without DNA",
                            ]
                        }
                    ],
                },
                "bio_spec_description": {"type": "string", "minLength": 1},
                "target_duration": {"type": "string", "minLength": 1},
                "number_groups_cohorts": {"type": "integer"},
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        # If schema validation passes, check other cases of validation
        data = request.json
        if data["study_type"] == "Interventional":
            required_fields = [
                "design_allocation",
                "design_intervention_model",
                "design_primary_purpose",
                "design_masking",
                "design_who_masked_list",
                "phase_list",
                "enrollment_count",
                "number_arms",
            ]

            for field in required_fields:
                if field not in data:
                    return (
                        ValidationError(
                            f"Field {field} is required for interventional studies"
                        ),
                        400,
                    )

        if data["study_type"] == "Observational":
            required_fields = [
                "design_observational_model_list",
                "design_time_perspective_list",
                "bio_spec_retention",
                "bio_spec_description",
                "enrollment_count",
                "enrollment_type",
                "target_duration",
                "number_groups_cohorts",
            ]

            for field in required_fields:
                if field not in data:
                    return (
                        ValidationError(
                            f"Field {field} is required for observational studies"
                        ),
                        400,
                    )

        study = Study.query.get(study_id)
        # Check user permissions
        if not is_granted("study_metadata", study):
            return "Access denied, you can not delete study", 403

        study_ = Study.query.get(study_id)

        study_.study_design.update(request.json)

        db.session.commit()

        return study_.study_design.to_dict()
