"""API routes for study eligibility metadata"""
from flask_restx import Resource, fields
from flask import request
from jsonschema import validate, ValidationError
from model import Study, db
from ..authentication import is_granted


from apis.study_metadata_namespace import api


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
        # Schema validation
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "gender": {"type": "string"},
                "gender_based": {"type": "string"},
                "gender_description": {"type": "string"},
                "minimum_age_value": {"type": "integer"},
                "maximum_age_value": {"type": "integer"},
                "minimum_age_unit": {"type": "string"},
                "maximum_age_unit": {"type": "string"},
                "healthy_volunteers": {"type": "string"},
                "inclusion_criteria": {"type": "array", "items": {"type": "string"}},
                "exclusion_criteria": {"type": "array", "items": {"type": "string"}},
                "study_population": {"type": "string"},
                "sampling_method": {"type": "string"},
            },
        }

        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        study_ = Study.query.get(study_id)
        # Check user permissions
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
