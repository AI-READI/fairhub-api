from flask_restx import fields

REDCapReportParticipantValuesDataModel = {
    "record_id": fields.String(
        required=True, readonly=True, description="Participant record ID"
    ),
    "studyid": fields.String(
        required=True, readonly=True, description="Study participant ID"
    ),
    "siteid": fields.String(required=True, readonly=True, description="Site ID"),
    "dm": fields.String(
        required=True, readonly=True, description="Data approved for Fairhub.io"
    ),
    "siteid": fields.String(required=True, readonly=True, description="Site ID"),
    "genderid": fields.String(
        required=True, readonly=True, description="Gender identity"
    ),
    "scrsex": fields.String(required=True, readonly=True, description="Sex at birth"),
    "race": fields.String(required=True, readonly=True, description="Race"),
    "race2": fields.String(
        required=True, readonly=True, description="Race further defined"
    ),
    "ethnic": fields.String(required=True, readonly=True, description="Ethnicity"),
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
        required=True, readonly=True, description="Participant disposition completed"
    ),
    "data_management_complete": fields.String(
        required=True, readonly=True, description="Fairhub.io data management completed"
    ),
    "current_medications_complete": fields.String(
        required=True, readonly=True, description="Current medications count"
    ),
    "current_medications": fields.Integer(
        required=True, readonly=True, description="Current medications completed"
    ),
    "dvenvyn": fields.String(
        required=True, readonly=True, description="Environmental sensor distributed"
    ),
    "dvenvstdat": fields.String(
        required=True,
        readonly=True,
        description="Date of environmental sensor distribution",
    ),
    "dvenvcrcid": fields.String(
        required=True,
        readonly=True,
        description="Was environmental sensor demonstrated?",
    ),
    "dvcgmyn": fields.String(
        required=True, readonly=True, description="Continuous glucose monitor inserted"
    ),
    "dvcgmstdat": fields.String(
        required=True,
        readonly=True,
        description="Date of continuous glucose monitor was inserted",
    ),
    "dvcgmvrfy": fields.String(
        required=True,
        readonly=True,
        description="Continuous glucose monitor initialized and recording?",
    ),
    "dvamwyn": fields.String(
        required=True,
        readonly=True,
        description="Was the Apple watch sent home with the participant?",
    ),
    "dvamwstdat": fields.String(
        required=True,
        readonly=True,
        description="Date Apple watch was given to participant",
    ),
    "dvamwsn": fields.String(
        required=True, readonly=True, description="Apple watch serial number"
    ),
    "dvrtmthd": fields.String(
        required=True, readonly=True, description="Planned method of device return"
    ),
    "dvrtnyn": fields.String(
        required=True,
        readonly=True,
        description="Was the participant given device return instructions and shipping materials?",
    ),
    "dvrtnship": fields.String(
        required=True, readonly=True, description="Return shipping tracking number"
    ),
    "mhterm_dm1": fields.String(
        required=True, readonly=True, description="Type I diabetes"
    ),
    "mhterm_dm2": fields.String(
        required=True, readonly=True, description="Type II diabetes"
    ),
    "mhterm_predm": fields.String(
        required=True, readonly=True, description="Pre-diabetes"
    ),
    "mh_dm_age": fields.String(
        required=True, readonly=True, description="Age diagnosed with type II diabetes"
    ),
    "mh_a1c": fields.String(
        required=True, readonly=True, description="Elevated A1C levels"
    ),
    "cmtrt_a1c": fields.String(
        required=True,
        readonly=True,
        description="Taking pills to control A1C and blood glucose levels?",
    ),
    "cmtrt_insln": fields.String(
        required=True,
        readonly=True,
        description="Injecting insulin to control blood glucose levels",
    ),
    "cmtrt_glcs": fields.String(
        required=True,
        readonly=True,
        description="Using other injectables to control blood glucose levels",
    ),
    "cmtrt_lfst": fields.String(
        required=True,
        readonly=True,
        description="Using lifestyle changes to control blood glucose levels",
    ),
    "scrcmpdat": fields.String(
        required=True, readonly=True, description="Screening survey completion date"
    ),
}
