import numpy as np

# Load API metadata from .env
# dotenv.load_dotenv()

# # Set REDCap API References
# REDCAP_API_TOKEN = os.environ["REDCAP_API_TOKEN"]
# REDCAP_API_URL = os.environ["REDCAP_API_URL"]

# Value assigned to missing values unless other specific value defined on function call
# (e.g. REDCapTransform.map_missing_values_by_columns(df, columns, new_missing_value))
missing_value_generic = "Value Unavailable"

# Utility Column Groups
index_columns = [
    "record_id",
]

# Data Column Groups
data_columns = [
    "studyid",
    "siteid",
    "dm",
    "genderid",
    "scrsex",
    "race",
    "race2",
    "ethnic",
    "dvenvyn",
    "dvenvstdat",
    "dvenvcrcid",
    "dvcgmyn",
    "dvcgmstdat",
    "dvcgmvrfy",
    "dvamwyn",
    "dvamwstdat",
    "dvamwsn",
    "dvrtmthd",
    "dvrtnyn",
    "dvrtnship",
    "mhterm_dm1",
    "mhterm_dm2",
    "mhterm_predm",
    "mh_dm_age",
    "mh_a1c",
    "cmtrt_a1c",
    "cmtrt_insln",
    "cmtrt_glcs",
    "cmtrt_lfst",
    "scrcmpdat",
]

# Survey Column Groups
survey_columns = [
    "screening_survey_complete",
    "study_enrollment_complete",
    "recruitment_survey_complete",
    "faq_survey_complete",
    "recruitment_survey_management_complete",
    "device_distribution_complete",
    "preconsent_survey_complete",
    "consent_survey_complete",
    "staff_consent_attestation_survey_complete",
    "demographics_survey_complete",
    "health_survey_complete",
    "substance_use_survey_complete",
    "cesd10_survey_complete",
    "paid5_dm_survey_complete",
    "diabetes_survey_complete",
    "dietary_survey_complete",
    "ophthalmic_survey_complete",
    "px_sdoh_combined_survey_complete",
    "px_food_insecurity_survey_complete",
    "px_neighborhood_environment_survey_complete",
    "px_racial_ethnic_discrimination_survey_complete",
    "decline_participation_survey_complete",
    "meds_assessment_complete",
    "driving_record_complete",
    "physical_assessment_complete",
    "bcva_complete",
    "photopic_mars_complete",
    "mesopic_mars_complete",
    "monofilament_complete",
    "moca_complete",
    "ecg_complete",
    "retinal_imaging_v2_complete",
    "lab_results_complete",
    "device_return_complete",
    "specimen_management_complete",
    "disposition_complete",
    "data_management_complete",
]

# Repeat Survey Column Groups
repeat_survey_columns = [
    "current_medications_complete",
]

repeat_survey_data_columns = ["current_medications_complete", "current_medications"]

#
# Value Maps
#

survey_instrument_map = {
    "2": "Complete",
    "1": "Unverified",
    "0": "Incomplete",
}

#
# REDCap Transform Config
#

redcapTransformConfig = {
    "reports": [
        (
            "dashboard_data_generic",
            {"report_id": 242544},
            [
                ("remap_values_by_columns", {"columns": data_columns}),
                ("map_missing_values_by_columns", {"columns": data_columns}),
                ("keep_columns", {"columns": index_columns + data_columns}),
            ],
        ),
        (
            "dashboard_data_overview",
            {"report_id": 251954},
            [
                (
                    "remap_values_by_columns",
                    {"columns": survey_columns, "value_map": survey_instrument_map},
                ),
                ("map_missing_values_by_columns", {"columns": survey_columns}),
                ("keep_columns", {"columns": index_columns + survey_columns}),
            ],
        ),
        (
            "dashboard_data_repeat_instruments",
            {"report_id": 259920},
            [
                ("drop_rows", {"columns": repeat_survey_columns}),
                (
                    "aggregate_repeat_instrument_column_by_index",
                    {"aggregator": np.max, "dtype": str},
                ),
                (
                    "keep_columns",
                    {"columns": index_columns + repeat_survey_data_columns},
                ),
            ],
        ),
    ],
    "merge_transformed_reports": (
        "dashboard_data_generic",
        [
            ("dashboard_data_overview", {"on": index_columns, "how": "inner"}),
            (
                "dashboard_data_repeat_instruments",
                {"on": index_columns, "how": "outer"},
            ),
        ],
    ),
    "post_merge_transforms": [
        (
            "remap_values_by_columns",
            {"columns": repeat_survey_columns, "value_map": survey_instrument_map},
        ),
        ("map_missing_values_by_columns", {"columns": repeat_survey_data_columns}),
    ],
    "index_columns": ["record_id"],
    "missing_value_generic": missing_value_generic,
}

#
# Visualization Transforms
#

# Sex & Gender Counts by Site
sexGenderTransformConfig = (
    "simpleTransform",
    {
        "key": "sex-and-gender",
        "strict": True,
        "transforms": {
            "name": "Sex & Gender",
            "vtype": "DoubleCategorical",
            "method": {
                "groups": ["siteid", "scrsex", "genderid"],
                "value": "record_id",
                "func": "count",
            },
            "accessors": {
                "filterby": {
                    "name": "Site",
                    "field": "siteid",
                    "missing_value": missing_value_generic,
                },
                "group": {
                    "name": "Sex",
                    "field": "scrsex",
                    "missing_value": missing_value_generic,
                    "astype": str,
                },
                "subgroup": {
                    "name": "Gender",
                    "field": "genderid",
                    "missing_value": missing_value_generic,
                    "astype": str,
                },
                "color": {
                    "name": "Gender",
                    "field": "genderid",
                    "missing_value": missing_value_generic,
                    "astype": str,
                },
                "value": {
                    "name": "Count (N)",
                    "field": "record_id",
                    "missing_value": missing_value_generic,
                    "astype": int,
                },
            },
        },
    },
)

# Race & Ethnicity Counts by Site
raceEthnicityTransformConfig = (
    "simpleTransform",
    {
        "key": "race-and-ethnicity",
        "strict": True,
        "transforms": {
            "name": "Race & Ethnicity",
            "vtype": "DoubleCategorical",
            "method": {
                "groups": ["siteid", "race", "ethnic"],
                "value": "record_id",
                "func": "count",
            },
            "accessors": {
                "filterby": {
                    "name": "Site",
                    "field": "siteid",
                    "missing_value": missing_value_generic,
                    "astype": str,
                },
                "group": {
                    "name": "Race",
                    "field": "race",
                    "missing_value": missing_value_generic,
                    "astype": str,
                },
                "subgroup": {
                    "name": "Ethnicity",
                    "field": "ethnic",
                    "missing_value": missing_value_generic,
                    "astype": str,
                },
                "color": {
                    "name": "Ethnicity",
                    "field": "ethnic",
                    "missing_value": missing_value_generic,
                    "astype": str,
                },
                "value": {
                    "name": "Count (N)",
                    "field": "record_id",
                    "missing_value": missing_value_generic,
                    "astype": int,
                },
            },
        },
    },
)

# Phenotypes
phenotypesTransformConfig = (
    "compoundTransform",
    {
        "key": "phenotype",
        "strict": True,
        "transforms": [
            {
                "name": "Prediabetes",
                "vtype": "SingleCategorical",
                "method": {
                    "groups": ["siteid", "mhterm_predm"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "name": "Prediabetes",
                        "field": "mhterm_predm",
                        "remap": lambda x: "Yes Prediabetes" if str(x["record"][x["accessors"]["group"]["field"]]) == "Yes" else "No Prediabetes",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Prediabetes",
                        "field": "mhterm_predm",
                        "remap": lambda x: "Yes Prediabetes" if str(x["record"][x["accessors"]["group"]["field"]]) == "Yes" else "No Prediabetes",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Type I Diabetes",
                "vtype": "SingleCategorical",
                "method": {
                    "groups": ["siteid", "mhterm_dm1"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "name": "Type I Diabetes",
                        "field": "mhterm_dm1",
                        "remap": lambda x: "Yes Type I Diabetes" if str(x["record"][x["accessors"]["group"]["field"]]) == "Yes" else "No Type I Diabetes",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Type I Diabetes",
                        "field": "mhterm_dm1",
                        "remap": lambda x: "Yes Type I Diabetes" if str(x["record"][x["accessors"]["group"]["field"]]) == "Yes" else "No Type I Diabetes",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Type II Diabetes",
                "vtype": "SingleCategorical",
                "method": {
                    "groups": ["siteid", "mhterm_dm2"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "name": "Type II Diabetes",
                        "field": "mhterm_dm2",
                        "remap": lambda x: "Yes Type II Diabetes" if str(x["record"][x["accessors"]["group"]["field"]]) == "Yes" else "No Type II Diabetes",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Type II Diabetes",
                        "field": "mhterm_dm2",
                        "remap": lambda x: "Yes Type II Diabetes" if str(x["record"][x["accessors"]["group"]["field"]]) == "Yes" else "No Type II Diabetes",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            }
        ],
    },
)

# Overview
overviewTransformConfig = (
    "compoundTransform",
    {
        "key": "overview",
        "strict": True,
        "transforms": [
            {
                "name": "Recruitment Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "recruitment_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Recruitment Survey",
                        "field": "recruitment_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Recruitment Survey",
                        "field": "recruitment_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Recruitment Survey",
                        "field": "recruitment_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "FAQ Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "faq_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "FAQ Survey",
                        "field": "faq_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "FAQ Survey",
                        "field": "faq_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "FAQ Survey",
                        "field": "faq_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Screening Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "screening_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Screening Survey",
                        "field": "screening_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Screening Survey",
                        "field": "screening_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Screening Survey",
                        "field": "screening_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Preconsent Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "preconsent_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Preconsent Survey",
                        "field": "preconsent_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Preconsent Survey",
                        "field": "preconsent_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Preconsent Survey",
                        "field": "preconsent_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Consent Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "consent_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Consent Survey",
                        "field": "consent_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Consent Survey",
                        "field": "consent_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Consent Survey",
                        "field": "consent_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Staff Consent Attestation Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "staff_consent_attestation_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Staff Consent Attestation Survey",
                        "field": "staff_consent_attestation_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Staff Consent Attestation Survey",
                        "field": "staff_consent_attestation_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Staff Consent Attestation Survey",
                        "field": "staff_consent_attestation_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Demographics Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "demographics_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Demographics Survey",
                        "field": "demographics_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Demographics Survey",
                        "field": "demographics_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Demographics Survey",
                        "field": "demographics_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Health Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "health_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Health Survey",
                        "field": "health_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Health Survey",
                        "field": "health_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Health Survey",
                        "field": "health_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Substance Use Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "substance_use_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Substance Use Survey",
                        "field": "substance_use_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Substance Use Survey",
                        "field": "substance_use_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Substance Use Survey",
                        "field": "substance_use_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "CES-D-10 Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "cesd10_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "CES-D-10 Survey",
                        "field": "cesd10_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "CES-D-10 Survey",
                        "field": "cesd10_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "CES-D-10 Survey",
                        "field": "cesd10_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "PAID-5 DM Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "paid5_dm_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "PAID-5 DM Survey",
                        "field": "paid5_dm_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "PAID-5 DM Survey",
                        "field": "paid5_dm_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "PAID-5 DM Survey",
                        "field": "paid5_dm_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Diabetes Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "diabetes_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Diabetes Survey",
                        "field": "diabetes_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Diabetes Survey",
                        "field": "diabetes_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Diabetes Survey",
                        "field": "diabetes_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Dietary Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "dietary_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Dietary Survey",
                        "field": "dietary_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Dietary Survey",
                        "field": "dietary_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Dietary Survey",
                        "field": "dietary_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Opthalmic Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "ophthalmic_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Opthalmic Survey",
                        "field": "ophthalmic_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Opthalmic Survey",
                        "field": "ophthalmic_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Opthalmic Survey",
                        "field": "ophthalmic_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "PhenX SDOH Combined Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "px_sdoh_combined_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "PhenX SDOH Combined Survey",
                        "field": "px_sdoh_combined_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "PhenX SDOH Combined Survey",
                        "field": "px_sdoh_combined_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "PhenX SDOH Combined Survey",
                        "field": "px_sdoh_combined_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "PhenX Food Insecurity Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "px_food_insecurity_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "PhenX Food Insecurity Survey",
                        "field": "px_food_insecurity_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "PhenX Food Insecurity Survey",
                        "field": "px_food_insecurity_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "PhenX Food Insecurity Survey",
                        "field": "px_food_insecurity_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "PhenX Neighborhood Environment Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "px_neighborhood_environment_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "PhenX Neighborhood Environment Survey",
                        "field": "px_neighborhood_environment_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "PhenX Neighborhood Environment Survey",
                        "field": "px_neighborhood_environment_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "PhenX Neighborhood Environment Survey",
                        "field": "px_neighborhood_environment_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "PhenX Racial and Ethnic Discrimination Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": [
                        "siteid",
                        "px_racial_ethnic_discrimination_survey_complete",
                    ],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "PhenX Racial and Ethnic Discrimination Survey",
                        "field": "px_racial_ethnic_discrimination_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "PhenX Racial and Ethnic Discrimination Survey",
                        "field": "px_racial_ethnic_discrimination_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "PhenX Racial and Ethnic Discrimination Survey",
                        "field": "px_racial_ethnic_discrimination_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Decline Participation Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "decline_participation_survey_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Decline Participation Survey",
                        "field": "decline_participation_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Decline Participation Survey",
                        "field": "decline_participation_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Decline Participation Survey",
                        "field": "decline_participation_survey_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Study Enrollment Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "study_enrollment_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Study Enrollment Survey",
                        "field": "study_enrollment_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Study Enrollment Survey",
                        "field": "study_enrollment_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Study Enrollment Survey",
                        "field": "study_enrollment_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Driving Record",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "driving_record_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Driving Record",
                        "field": "driving_record_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Driving Record",
                        "field": "driving_record_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Driving Record",
                        "field": "driving_record_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Device Distribution",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "device_distribution_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Device Distribution",
                        "field": "device_distribution_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Device Distribution",
                        "field": "device_distribution_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Device Distribution",
                        "field": "device_distribution_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Medications Assessment",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "meds_assessment_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Medications Assessment",
                        "field": "meds_assessment_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Medications Assessment",
                        "field": "meds_assessment_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Medications Assessment",
                        "field": "meds_assessment_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Physical Assessment",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "physical_assessment_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Physical Assessment",
                        "field": "physical_assessment_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Physical Assessment",
                        "field": "physical_assessment_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Physical Assessment",
                        "field": "physical_assessment_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "BCVA",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "bcva_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "BCVA",
                        "field": "bcva_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "BCVA",
                        "field": "bcva_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "BCVA",
                        "field": "bcva_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Photopic MARS",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "photopic_mars_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Photopic MARS",
                        "field": "photopic_mars_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Photopic MARS",
                        "field": "photopic_mars_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Photopic MARS",
                        "field": "photopic_mars_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Mesopic MARS",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "mesopic_mars_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Mesopic MARS",
                        "field": "mesopic_mars_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Mesopic MARS",
                        "field": "mesopic_mars_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Mesopic MARS",
                        "field": "mesopic_mars_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Monofilament",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "monofilament_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Monofilament",
                        "field": "monofilament_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Monofilament",
                        "field": "monofilament_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Monofilament",
                        "field": "monofilament_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "MOCA",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "moca_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "MOCA",
                        "field": "moca_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "MOCA",
                        "field": "moca_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "MOCA",
                        "field": "moca_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "ECG Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "ecg_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "ECG Survey",
                        "field": "ecg_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "ECG Survey",
                        "field": "ecg_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "ECG Survey",
                        "field": "ecg_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Lab Results Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "lab_results_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Lab Results Survey",
                        "field": "lab_results_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Lab Results Survey",
                        "field": "lab_results_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Lab Results Survey",
                        "field": "lab_results_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Specimen Management",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "specimen_management_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Specimen Management",
                        "field": "specimen_management_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Specimen Management",
                        "field": "specimen_management_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Specimen Management",
                        "field": "specimen_management_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Device Return",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "device_return_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Device Return",
                        "field": "device_return_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Device Return",
                        "field": "device_return_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Device Return",
                        "field": "device_return_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Disposition Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "disposition_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Disposition Survey",
                        "field": "disposition_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Disposition Survey",
                        "field": "disposition_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Disposition Survey",
                        "field": "disposition_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
            {
                "name": "Data Management Survey",
                "vtype": "DoubleCategorical",
                "method": {
                    "groups": ["siteid", "data_management_complete"],
                    "value": "record_id",
                    "func": "count",
                },
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "remap": lambda x: x["name"],
                        "name": "Data Management Survey",
                        "field": "data_management_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Data Management Survey",
                        "field": "data_management_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Data Management Survey",
                        "field": "data_management_complete",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
        ],
    },
)
transformConfigs = {
    "redcap": redcapTransformConfig,
    "overview": overviewTransformConfig,
    "phenotypes": phenotypesTransformConfig,
    "devices": phenotypesTransformConfig,
    "recruitment": phenotypesTransformConfig,
}
