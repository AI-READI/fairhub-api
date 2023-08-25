from model import Study

from flask_restx import Namespace, Resource, fields


from apis.study_metadata_namespace import api


study_eligibility = api.model(
    "StudyEligibility",
    {
        "id": fields.String(required=True),
        "gender": fields.String(required=True),
        "gender_based": fields.Boolean(required=True),
        "gender_description": fields.String(required=True),
        "minimum_age": fields.String(required=True),
        "maximum_age": fields.String(required=True),
        "healthy_volunteers": fields.Boolean(required=True),
        "inclusion_criteria": fields.List(fields.String, required=True),
        "exclusion_criteria": fields.List(fields.String, required=True),
        "study_population": fields.String(required=True),
        "sampling_method": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/metadata/eligibility")
class StudyEligibilityResource(Resource):
    @api.doc("list_study")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_eligibility)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_eligibility_ = study_.study_eligibility
        return [s.to_dict() for s in study_eligibility_]
