from flask_restx import Resource, fields
from model import Study, db, StudyEligibility
from flask import request


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
    },
)


@api.route("/study/<study_id>/metadata/eligibility")
class StudyEligibilityResource(Resource):
    @api.doc("eligibility")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The study identifier")
    @api.marshal_with(study_eligibility)
    def get(self, study_id: int):
        study_ = Study.query.get(study_id)
        study_eligibility_ = study_.study_eligibility
        return study_eligibility_.to_dict()

    def post(self, study_id: int):
        data = request.json
        study_eligibility_ = Study.query.get(study_id)
        study_eligibility_ = StudyEligibility.from_data(study_eligibility_, data)
        db.session.add(study_eligibility_)
        db.session.commit()
        return study_eligibility_.to_dict()

    @api.route("/study/<study_id>/metadata/eligibility/<eligibility_id>")
    class StudyArmUpdate(Resource):
        def put(self, study_id: int, eligibility_id: int):
            study_eligibility_ = StudyEligibility.query.get(eligibility_id)
            study_eligibility_.update(request.json)
            db.session.commit()
            return study_eligibility_.to_dict()
