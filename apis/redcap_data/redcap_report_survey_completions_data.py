"""API routes for redcap report survey completions data"""
# import typing

# from flask import request
from flask_restx import Resource, fields

# from jsonschema import ValidationError, validate

import model
from apis.redcap_data_namespace import api

# from ..authentication import is_granted

# # REDCap Data Visualization ETL Configuration
# from modules.etl.config import redcapTransformConfig
# from modules.etl.config import sexGenderTransformConfig
# from modules.etl.config import raceEthnicityTransformConfig
# from modules.etl.config import phenotypeTransformConfig
# from modules.etl.config import studyWaypointsTransformConfig

# # ETL Modules
# from modules.etl import transforms


# Import In-Memory Cache
# from __main__ import IN_MEMORY_CACHE

redcap_report_survey_completions_data = api.model(
    "RedcapReportSurveyCompletionsData",
    {
        "record_id": fields.String(
            required=True, readonly=True, description="Participant record ID"
        ),
        "studyid": fields.String(
            required=True, readonly=True, description="Study participant ID"
        ),
        "screening_survey_complete": fields.String(
            required=True, readonly=True, description="Screening survey completed"
        ),
        "study_enrollment_complete": fields.String(
            required=True, readonly=True, description="Study enrollment completed"
        ),
        "recruitment_survey_complete": fields.String(
            required=True, readonly=True, description="Recruitment survey completed"
        ),
        "faq_survey_complete": fields.String(
            required=True, readonly=True, description="FAQ survey completed"
        ),
        "recruitment_survey_management_complete": fields.String(
            required=True,
            readonly=True,
            description="Recruitment survey management completed",
        ),
        "device_distribution_complete": fields.String(
            required=True, readonly=True, description="Device distribution completed"
        ),
        "preconsent_survey_complete": fields.String(
            required=True, readonly=True, description="Pre-consent survey completed"
        ),
        "consent_survey_complete": fields.String(
            required=True, readonly=True, description="Consent survey completed"
        ),
        "staff_consent_attestation_survey_complete": fields.String(
            required=True,
            readonly=True,
            description="Staff consent attestation survey completed",
        ),
        "demographics_survey_complete": fields.String(
            required=True, readonly=True, description="Demographics survey completed"
        ),
        "health_survey_complete": fields.String(
            required=True, readonly=True, description="Health survey completed"
        ),
        "substance_use_survey_complete": fields.String(
            required=True, readonly=True, description="Substance use survey completed"
        ),
        "cesd10_survey_complete": fields.String(
            required=True, readonly=True, description="CES-D-10 survey completed"
        ),
        "paid5_dm_survey_complete": fields.String(
            required=True, readonly=True, description="PAID-5 DM survey completed"
        ),
        "diabetes_survey_complete": fields.String(
            required=True, readonly=True, description="Diabetes survey completed"
        ),
        "dietary_survey_complete": fields.String(
            required=True, readonly=True, description="Dietary survey completed"
        ),
        "ophthalmic_survey_complete": fields.String(
            required=True, readonly=True, description="Opthalmic survey completed"
        ),
        "px_sdoh_combined_survey_complete": fields.String(
            required=True, readonly=True, description="PhenX SDOH survey completed"
        ),
        "px_food_insecurity_survey_complete": fields.String(
            required=True,
            readonly=True,
            description="PhenX Food Insecurity survey completed",
        ),
        "px_neighborhood_environment_survey_complete": fields.String(
            required=True,
            readonly=True,
            description="PhenX Neighborhood Enviroment survey completed",
        ),
        "px_racial_ethnic_discrimination_survey_complete": fields.String(
            required=True,
            readonly=True,
            description="PhenX Racial/Ethnic Discrimination survey completed",
        ),
        "decline_participation_survey_complete": fields.String(
            required=True,
            readonly=True,
            description="Decline participation survey completed",
        ),
        "meds_assessment_complete": fields.String(
            required=True, readonly=True, description="Medications assessment completed"
        ),
        "driving_record_complete": fields.String(
            required=True, readonly=True, description="Driving record completed"
        ),
        "physical_assessment_complete": fields.String(
            required=True, readonly=True, description="Physical assessment completed"
        ),
        "bcva_complete": fields.String(
            required=True, readonly=True, description="BCVA completed"
        ),
        "photopic_mars_complete": fields.String(
            required=True, readonly=True, description="Photopic mars completed"
        ),
        "mesopic_mars_complete": fields.String(
            required=True, readonly=True, description="Mesopic mars completed"
        ),
        "monofilament_complete": fields.String(
            required=True, readonly=True, description="Monofilament completed"
        ),
        "moca_complete": fields.String(
            required=True, readonly=True, description="MOCA instrument completed"
        ),
        "ecg_complete": fields.String(
            required=True, readonly=True, description="ECG completed"
        ),
        "retinal_imaging_v2_complete": fields.String(
            required=True, readonly=True, description="Retinal imaging completed"
        ),
        "lab_results_complete": fields.String(
            required=True, readonly=True, description="Lab results completed"
        ),
        "device_return_complete": fields.String(
            required=True, readonly=True, description="Device return completed"
        ),
        "specimen_management_complete": fields.String(
            required=True, readonly=True, description="Specimen management completed"
        ),
        "disposition_complete": fields.String(
            required=True,
            readonly=True,
            description="Participant disposition completed",
        ),
        "data_management_complete": fields.String(
            required=True,
            readonly=True,
            description="Fairhub.io data management completed",
        ),
    },
)


@api.route("/study/<study_id>/redcap/<redcap_project_id>/survey-completions")
class RedcapReportSurveyCompletionsDataResource(Resource):
    @api.doc("report_survey_completions_data")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(redcap_report_survey_completions_data)
    # @IN_MEMORY_CACHE.cached()
    def get(self, study_id: int, redcap_project_id: str):
        study_ = model.Study.query.get(study_id)
        study_redcap_ = study_.study_redcap.to_dict()
        PyCapProject = Project(
            study_redcap_["redcap_api_url"], study_redcap_["redcap_api_token"]
        )
        survey_completions = PyCapProject.export_report(
            study_redcap_["redcap_report_id_survey_completions"]
        )
        return survey_completions
