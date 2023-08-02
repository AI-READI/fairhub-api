"""
Each function definition encapsulates a transform
on REDCap data for a visualization module. The
transformed data is intended to be cached as a
JSON object in Redis.
"""

import pandas as pd
import os
import re

DEV_SAMPLE_REPORT_DATA = os.environ["DEV_SAMPLE_REPORT_DATA"]

base_cols = [
    "record_id",
    "siteid",
    "dm",
    "redcap_repeat_instrument",
    "redcap_repeat_instance",
    "redcap_data_access_group",
]

numeric_cols = [

]

dm_map = {
    "i",
    "d",
}

demographics_cols = [
    "genderid",
    "genderidot",
    "scrsex",
    "scrsexot",
    "race",
    "raceot",
    "race2",
    "ethnic",
    "ethnicot",
    "ancestry",
]

gender_map = {
    "0"         : "",
    "1"         : "",
    "2"         : "",
}

race_map = {
    "c17459"    : "American Indian or Alaska Native",
    "c41260"    : "Asian",
    "c16352"    : "Black or African American",
    "c77820"    : "Middle Eastern",
    "c41219"    : "Native Hawaiian or Pacific Islander",
    "c77813"    : "North African",
    "c41261"    : "White or Caucasian",
    "888"       : "Other race, ethnicity, or origin",
    "777"       : "Prefer not to say",
}

ethnicity_map = {
    "c41222"    : "No",
    "c67113"    : "Yes, Mexican",
    "c67112"    : "Yes, Puerto Rican",
    "c107608"   : "Yes, Cuban",
    "c67117"    : "Yes, Dominican Republic",
    "c67118"    : "Yes, Central American",
    "c126532"   : "Yes, South American",
    "c999"      : "Yes, Chicano",
    "888"       : "Yes, Other",
    "777"       : "Prefer not to say",
}

contact_cols = [
    "cnct_sccs",
    "cnct_type",
    "cnct_prp",
]

phenotype_cols = [
    "mhterm_dm1",
    "mhterm_dm2",
    "mhterm_predm",
    "mh_dm_age",
    "mh_a1c",
    "cmtrt_a1c",
    "cmtrt_insln",
    "cmtrt_glcs",
    "cmtrt_lfst",
]

device_cols = [
    "dvenvyn",
    "dvenvstdat",
    "dvenvreasn",
    "dvenvcrcid",
    "dvcgmyn",
    "dvcgmstdat",
    "dvcgmreasn",
    "dvcgmvrfy",
    "dvamwyn",
    "dvamwstdat",
    "dvamwreasn",
    "dvamwsn",
    "dvrtmthd",
    "dvrtnyn",
    "dvrtnship",
]

survey_cols = [
    "recstartts",
    "recruitment_survey_complete",
    "faqstartts",
    "faq_survey_complete",
    "scrstartts",
    "screening_survey_complete",
    "preconstartts",
    "preconsent_survey_complete",
    "icfsvyts",
    "consent_survey_complete",
    "dmgstartts",
    "demographics_survey_complete",
    "mhstartts",
    "health_survey_complete",
    "sustartts",
    "substance_use_survey_complete",
    "cesstartts",
    "cesd10_survey_complete",
    "paidstartts",
    "paid5_dm_survey_complete",
    "dmlstartts",
    "diabetes_survey_complete",
    "dietstartts",
    "dietary_survey_complete",
    "viastartts",
    "ophthalmic_survey_complete",
    "pxsdohstartts",
    "px_sdoh_combined_survey_complete",
    "pxfistartts",
    "px_food_insecurity_survey_complete",
    "pxnestartts",
    "px_neighborhood_environment_survey_complete",
    "pxrdstartts",
    "px_racial_ethnic_discrimination_survey_complete",
    "declinestartts",
    "decline_participation_survey_complete",
    "study_enrollment_complete",
    "recruitment_survey_management_complete",
    "device_distribution_complete",
    "staff_consent_attestation_survey_complete",
    "meds_assessment_complete",
    "driving_record_complete",
    "current_medications_complete",
    "physical_assessment_complete",
    "bcva_complete",
    "photopic_mars_complete",
    "mesopic_mars_complete",
    "monofilament_complete",
    "moca_complete",
    "ecg_complete",
    "retinal_imaging_complete",
    "lab_results_complete",
    "device_return_complete",
    "specimen_management_complete",
    "disposition_complete",
    "data_management_complete",
]

# def __preprocess (data):
#     """
#     Generic pre-processing for all modules
#     """
#     df = pd.read_csv(DEV_SAMPLE_REPORT_DATA, sep = "\t", dtype = "str")
#     for column in df.columns:
#         for val in df[column]:
#             if re.match(r"[0-9]{1,32}", val):


#     return data

def overview (data):
    """
    Study overview transform

    Target Schema - Sankey
    [
        {
            source: "State A",
            target: "State C",
            value: 16
        },
        {
            source: "State B",
            target: "State C",
            value: 2
        },
        {
            source: "State A",
            target: "State D",
            value: 4
        },
        {
            source: "State C",
            target: "State D",
            value: 18
        }
    ]

    Target Schema - Doughnut
    [
        {
            group: "State A",
            value: 141
        },
        {
            group: "State B",
            value: 221
        }
    ]
    """
    cols = base_cols + phenotype_cols + demongraphics_cols + survey_cols
    df = pd.read_csv(DEV_SAMPLE_REPORT_DATA, sep = "\t", dtype = "str")[cols]
    return data

def progress (data):
    """
    Study protocol transform
    """
    cols = base_cols + phenotype_cols + demongraphics_cols + survey_cols
    df = pd.read_csv(DEV_SAMPLE_REPORT_DATA, sep = "\t", dtype = "str")[cols]
    return data

def demographics (data):
    """
    Study demographics transform
    """
    cols = base_cols + phenotype_cols + demographics_cols
    df = pd.read_csv(DEV_SAMPLE_REPORT_DATA, sep = "\t", dtype = "str")[cols]
    return data

def phenotype (data):
    """
    Study phenotype transform
    """
    cols = base_cols + phenotype_cols
    df = pd.read_csv(DEV_SAMPLE_REPORT_DATA, sep = "\t", dtype = "str")[cols]
    return data

def device (data):
    """
    Study device transform
    """
    cols = base_cols + phenotype_cols + demographics_cols + device_cols
    df = pd.read_csv(DEV_SAMPLE_REPORT_DATA, sep = "\t", dtype = "str")[cols]
    return data

def contact (data):
    """
    Study contact transform
    """
    cols = base_cols + survey_cols + device_cols + contact_cols
    df = pd.read_csv(DEV_SAMPLE_REPORT_DATA, sep = "\t", dtype = "str")[cols]
    return data
