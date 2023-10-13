from transforms import REDCapTransform, ModuleTransform
import numpy as np

if __name__ == "__main__":
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
        "redcap_api_url": "https://redcap.iths.org/api/",
        "redcap_api_key": "5508FE11E75105E0DB976205AA27DDA3",
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
                "dashboard_data_study_waypoints",
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
                (
                    "dashboard_data_study_waypoints",
                    {"on": index_columns, "how": "inner"},
                ),
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
    sexGenderTransform = (
        "simpleTransform",
        {
            "key": "sex-and-gender-transform",
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
    raceEthnicityTransform = (
        "simpleTransform",
        {
            "key": "race-and-ethnicity-transform",
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
    phenotypeTransform = (
        "simpleTransform",
        {
            "key": "phenotype-transform",
            "strict": True,
            "transforms": {
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
                        "name": "Phenotype",
                        "field": "mhterm_dm2",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Phenotype",
                        "field": "mhterm_dm2",
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

    # Study Waypoints
    studyWaypointsTransform = (
        "compoundTransform",
        {
            "key": "study-waypoints-transform",
            "strict": True,
            "transforms": [
                {
                    "name": "Recruitment Survey",
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
                    "method": {
                        "groups": [
                            "siteid",
                            "staff_consent_attestation_survey_complete",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
                    "method": {
                        "groups": [
                            "siteid",
                            "px_neighborhood_environment_survey_complete",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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
                    "vtype": "SingleCategorical",
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

    # Sex & Gender Counts by Site
    mixedTransform = (
        "mixedTransform",
        {
            "key": "mixed-transform-test",
            "strict": True,
            "transforms": [
                {
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
                {
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
                            "name": "Phenotype",
                            "field": "mhterm_dm2",
                            "missing_value": missing_value_generic,
                            "astype": str,
                        },
                        "color": {
                            "name": "Phenotype",
                            "field": "mhterm_dm2",
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

    extract = REDCapTransform(config=redcapTransformConfig).merged

    extract.to_csv("merged-transform.tsv", sep="\t")

    transforms = [
        sexGenderTransform,
        raceEthnicityTransform,
        phenotypeTransform,
        studyWaypointsTransform,
        mixedTransform,
    ]

    # Print
    for module_method, config in transforms:
        transformer = getattr(ModuleTransform(config), module_method)(extract)
        if type(transformer.transformed) == list:
            for record in transformer.transformed:
                print(record)
            print("\n")
        if type(transformer.transformed) == dict:
            for key, transform in transformer.transformed.items():
                print(key)
                for record in transform:
                    print(record)
else:
    pass
