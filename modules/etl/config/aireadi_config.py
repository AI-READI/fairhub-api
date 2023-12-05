from typing import Any, Dict, List, Tuple
import numpy as np
from datetime import datetime

# Load API metadata from .env
# dotenv.load_dotenv()

# # Set REDCap API References
# REDCAP_API_TOKEN = os.environ["REDCAP_API_TOKEN"]
# REDCAP_API_URL = os.environ["REDCAP_API_URL"]

# Value assigned to missing values unless other specific value defined on function call
# (e.g. REDCapTransform.map_missing_values_by_columns(df, columns, new_missing_value))
missing_value_generic: str = "Value Unavailable"

# Utility Column Groups
index_columns: List = [
    "record_id",
]

# Data Column Groups
data_columns: List = [
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

computed_columns: List = [
    "phenotype",
    "treatments",
]

# Survey Column Groups
survey_columns: List = [
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
repeat_survey_columns: List = [
    "current_medications_complete",
]

repeat_survey_data_columns: List = [
    "current_medications_complete",
    "current_medications"
]

#
# Value Maps
#

survey_instrument_map: Dict[str, str] = {
    "2": "Complete",
    "1": "Unverified",
    "0": "Incomplete",
}

phenotype_column_map: Dict[str, str] = {
    "mhterm_dm2": "Type II Diabetes",
    "mhterm_predm": "Prediabetes",
    "mh_a1c": "Elevated A1C",
}

treatments_column_map: Dict[str, str] = {
    "cmtrt_a1c": "Oral Medication",
    "cmtrt_glcs": "Non-Insulin Injectable",
    "cmtrt_insln": "Insuling Injectable",
    "cmtrt_lfst": "Lifestyle Management"
}

#
# REDCap Transform Config
#

# Note: The REDCap report_id is matched to the transform
# by the value of the key property in the report dictionary.
redcapTransformConfig: Dict[str, List[Any]|Tuple[str, List[Any]]|str|List] = {
    "reports": [
        {
            "key": "participant-value",
            "kwdargs": {},
            "transforms": [
                ("remap_values_by_columns", {"columns": data_columns}),
                ("map_missing_values_by_columns", {"columns": data_columns}),
                ("new_column_from_binary_columns_positive_class", {"column_name_map": phenotype_column_map, "new_column_name": "phenotype"}),
                ("new_column_from_binary_columns_positive_class", {"column_name_map": treatments_column_map, "new_column_name": "treatments"}),
                ("keep_columns", {"columns": index_columns + data_columns + computed_columns}),
            ],
        },
        {
            "key": "instrument-status",
            "kwdargs": {},
            "transforms": [
                ("remap_values_by_columns", {"columns": survey_columns, "value_map": survey_instrument_map}),
                ("map_missing_values_by_columns", {"columns": survey_columns}),
                ("keep_columns", {"columns": index_columns + survey_columns}),
            ],
        },
        {
            "key": "repeat-instrument",
            "kwdargs": {},
            "transforms": [
                ("drop_rows", {"columns": repeat_survey_columns}),
                ("aggregate_repeat_instrument_by_index", {"aggregator": np.max, "dtype": str}),
                ("keep_columns", {"columns": index_columns + repeat_survey_data_columns}),
            ],
        },
    ],
    "post_transform_merge": (
        "participant-value", [
            # ("participant-value", {"on": index_columns, "how": "inner"}),
            ("instrument-status", {"on": index_columns, "how": "inner"}),
            ("repeat-instrument", {"on": index_columns, "how": "outer"}),
            # ("repeat-instrument", {"on": index_columns, "how": "outer"}),
        ],
    ),
    "post_merge_transforms": [
        ("remap_values_by_columns",{"columns": repeat_survey_columns, "value_map": survey_instrument_map}),
        ("map_missing_values_by_columns", {"columns": repeat_survey_data_columns}),
    ],
    "index_columns": ["record_id"],
    "missing_value_generic": missing_value_generic,
}

#
# Visualization Transforms
#

# Overview
overviewTransformConfig: Tuple[str, Dict[str, Any]] = (
    "compoundTransform",
    {
        "key": "overview",
        "strict": True,
        "transforms": [
            {
                "name": "Recruitment Survey",
                "vtype": "DoubleCategorical",
                "methods": [
                    {
                        "groups": ["siteid", "recruitment_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "faq_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "screening_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "preconsent_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "consent_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": [
                            "siteid",
                            "staff_consent_attestation_survey_complete",
                        ],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "demographics_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "health_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "substance_use_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "cesd10_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "paid5_dm_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "diabetes_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "dietary_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "ophthalmic_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "px_sdoh_combined_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "px_food_insecurity_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": [
                            "siteid",
                            "px_neighborhood_environment_survey_complete",
                        ],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": [
                            "siteid",
                            "px_racial_ethnic_discrimination_survey_complete",
                        ],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "decline_participation_survey_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "study_enrollment_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "driving_record_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "device_distribution_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "meds_assessment_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "physical_assessment_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "bcva_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "photopic_mars_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "mesopic_mars_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "monofilament_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "moca_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "ecg_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "lab_results_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "specimen_management_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "device_return_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "disposition_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
                "methods": [
                    {
                        "groups": ["siteid", "data_management_complete"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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

# Recruitment Counts by Site
recruitmentTransformConfig: Tuple[str, Dict[str, Any]] = (
    "simpleTransform",
    {
        "key": "recruitment",
        "strict": True,
        "transforms": [
            {
                "name": "Recruitment",
                "vtype": "DoubleDiscrete",
                "methods": [
                    {
                        "groups": ["siteid", "race", "scrcmpdat"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astyoe": str,
                    },
                    "subgroup": {
                        "name": "Race",
                        "field": "race",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Race",
                        "field": "race",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "x": {
                        "name": "Week of the Year",
                        "field": "scrcmpdat",
                        "missing_value": missing_value_generic,
                        "astype": int,
                        "remap": lambda x: datetime.strptime(x["record"][x["accessors"]["x"]["field"]], "%Y-%m-%d").isocalendar().week
                    },
                    "y": {
                        "name": "Cumulative Count (N)",
                        "field": "record_id",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            },
        ]
    },
)

# Race & Ethnicity Counts by Site
raceEthnicityTransformConfig: Tuple[str, Dict[str, Any]] = (
    "simpleTransform",
    {
        "key": "race-ethnicity",
        "strict": True,
        "transforms": [
            {
                "name": "Race & Ethnicity",
                "vtype": "DoubleCategorical",
                "methods": [
                    {
                        "groups": ["siteid", "race", "ethnic"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
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
        ]
    },
)

# Sex & Gender Counts by Site
sexGenderTransformConfig: Tuple[str, Dict[str, Any]] = (
    "simpleTransform",
    {
        "key": "sex-gender",
        "strict": True,
        "transforms": [
            {
                "name": "Sex & Gender",
                "vtype": "DoubleCategorical",
                "methods": [
                    {
                        "groups": ["siteid", "scrsex", "genderid"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                    },
                    "group": {
                        "name": "Gender",
                        "field": "genderid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "subgroup": {
                        "name": "Sex",
                        "field": "scrsex",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Sex",
                        "field": "scrsex",
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
        ]
    },
)

# # Phenotypes
# phenotypesTransformConfig: Tuple[str, Dict[str, Any]] = (
#     "compoundTransform",
#     {
#         "key": "phenotype",
#         "strict": True,
#         "transforms": [
#             {
#                 "name": "Prediabetes",
#                 "vtype": "SingleCategorical",
#                 "methods": [
#                     {
#                         "groups": ["siteid", "mhterm_predm"],
#                         "value": "record_id",
#                         "func": "count",
#                     }
#                 ],
#                 "accessors": {
#                     "filterby": {
#                         "name": "Site",
#                         "field": "siteid",
#                         "missing_value": missing_value_generic,
#                         "astype": str,
#                     },
#                     "group": {
#                         "name": "Prediabetes",
#                         "field": "mhterm_predm",
#                         "remap": lambda x: "Prediabetes"
#                         if str(x["record"][x["accessors"]["group"]["field"]]) == "Yes"
#                         else "No",
#                         "missing_value": missing_value_generic,
#                         "astype": str,
#                     },
#                     "color": {
#                         "name": "Prediabetes",
#                         "field": "mhterm_predm",
#                         "remap": lambda x: "Prediabetes"
#                         if str(x["record"][x["accessors"]["group"]["field"]]) == "Yes"
#                         else "No",
#                         "missing_value": missing_value_generic,
#                         "astype": str,
#                     },
#                     "value": {
#                         "name": "Count (N)",
#                         "field": "record_id",
#                         "missing_value": missing_value_generic,
#                         "astype": int,
#                     },
#                 },
#             },
#             {
#                 "name": "Type I Diabetes",
#                 "vtype": "SingleCategorical",
#                 "methods": [
#                     {
#                         "groups": ["siteid", "mhterm_dm1"],
#                         "value": "record_id",
#                         "func": "count",
#                     }
#                 ],
#                 "accessors": {
#                     "filterby": {
#                         "name": "Site",
#                         "field": "siteid",
#                         "missing_value": missing_value_generic,
#                         "astype": str,
#                     },
#                     "group": {
#                         "name": "Type I Diabetes",
#                         "field": "mhterm_dm1",
#                         "remap": lambda x: "Type I Diabetes"
#                         if str(x["record"][x["accessors"]["group"]["field"]]) == "Yes"
#                         else "No",
#                         "missing_value": missing_value_generic,
#                         "astype": str,
#                     },
#                     "color": {
#                         "name": "Type I Diabetes",
#                         "field": "mhterm_dm1",
#                         "remap": lambda x: "Type I Diabetes"
#                         if str(x["record"][x["accessors"]["group"]["field"]]) == "Yes"
#                         else "No",
#                         "missing_value": missing_value_generic,
#                         "astype": str,
#                     },
#                     "value": {
#                         "name": "Count (N)",
#                         "field": "record_id",
#                         "missing_value": missing_value_generic,
#                         "astype": int,
#                     },
#                 },
#             },
#             {
#                 "name": "Type II Diabetes",
#                 "vtype": "SingleCategorical",
#                 "methods": [
#                     {
#                         "groups": ["siteid", "mhterm_dm2"],
#                         "value": "record_id",
#                         "func": "count",
#                     }
#                 ],
#                 "accessors": {
#                     "filterby": {
#                         "name": "Site",
#                         "field": "siteid",
#                         "missing_value": missing_value_generic,
#                         "astype": str,
#                     },
#                     "group": {
#                         "name": "Type II Diabetes",
#                         "field": "mhterm_dm2",
#                         "remap": lambda x: "Type II Diabetes"
#                         if str(x["record"][x["accessors"]["group"]["field"]]) == "Yes"
#                         else "No",
#                         "missing_value": missing_value_generic,
#                         "astype": str,
#                     },
#                     "color": {
#                         "name": "Type II Diabetes",
#                         "field": "mhterm_dm2",
#                         "remap": lambda x: "Type II Diabetes"
#                         if str(x["record"][x["accessors"]["group"]["field"]]) == "Yes"
#                         else "No",
#                         "missing_value": missing_value_generic,
#                         "astype": str,
#                     },
#                     "value": {
#                         "name": "Count (N)",
#                         "field": "record_id",
#                         "missing_value": missing_value_generic,
#                         "astype": int,
#                     },
#                 },
#             },
#         ],
#     },
# )

# Phenotypes
phenotypesTransformConfig: Tuple[str, Dict[str, Any]] = (
    "compoundTransform",
    {
        "key": "phenotype",
        "strict": True,
        "transforms": [
            {
                "name": "Phenotype",
                "vtype": "SingleCategorical",
                "methods": [
                    {
                        "groups": ["siteid", "phenotype"],
                        "value": "record_id",
                        "func": "count",
                    }
                ],
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "name": "Phenotype",
                        "field": "phenotype",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Phenotype",
                        "field": "mhterm_predm",
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

currentMedicationsTransformConfig: Tuple[str, Dict[str, Any]] = (
    "simpleTransform",
    {
        "key": "current-medications",
        "strict": True,
        "transforms": [
            {
                "name": "Current Medications",
                "vtype": "SingleCategorical",
                "methods": [
                    {
                        "groups": ["siteid"],
                        "value": "current_medications",
                        "func": "count",
                    }
                ],
                "accessors": {
                    "filterby": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "group": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "color": {
                        "name": "Site",
                        "field": "siteid",
                        "missing_value": missing_value_generic,
                        "astype": str,
                    },
                    "value": {
                        "name": "Current Medications (N)",
                        "field": "current_medications",
                        "missing_value": missing_value_generic,
                        "astype": int,
                    },
                },
            }
        ]
    },
)


transformConfigs: Dict[str, Any] = {
    "redcap": redcapTransformConfig,
    "overview": overviewTransformConfig,
    "recruitment": recruitmentTransformConfig,
    "race-ethnicity": raceEthnicityTransformConfig,
    "sex-gender": sexGenderTransformConfig,
    "phenotypes": phenotypesTransformConfig,
    "current-medications": currentMedicationsTransformConfig,
}
