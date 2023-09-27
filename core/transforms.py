"""
Each function definition encapsulates a transform
on REDCap data for a visualization module. The
transformed data is intended to be cached as a
JSON object in Redis.
"""

import pandas as pd
import numpy as np
import os
import re
import typing

class REDCapTransform (object):
    """
    A class to transform data from REDCap

    Design Criteria
    - The class is configurable to any REDCap instance
    - The class has a defined transform precedence
    - The transform precedence is: column group, column, column value
    - The transforms are executed as a stack following this precendence
    - The transforms are idempotent
    """
    def __init__ (self,
        df: pd.DataFrame,
        config: dict,
    ):
        self.df                     = df
        self.config                 = config
        self.checkbox_colname_maps  = {}
        self.radio_colname_maps     = {}


    #
    # Data Frame Setup Methods
    #

    #
    # Data Frame Setup Methods
    #

    def preprocess_checkbox_conditional (self, df: pd.DataFrame, checkbox_key_value: dict, by_column_value: dict, checkbox_to_value: typing.Any = np.nan) -> pd.DataFrame:
        return df

    def __preprocess_checkbox_columns (self, df: pd.DataFrame, maps: list = [], dtype: typing.Any = np.float64, nonetype: typing.Any = np.nan) -> pd.DataFrame:
        """
        Pre-processing for checkbox columns
        - Sanitize column names
        - Type columns as ints
        - IF CHECKBOX IS 0, NEED TO CHECK FORM DATE TO ENSURE 0 IS VALID OF A DEFAULT (i.e. UNASSIGNED)
        """

        # Map Checkbox Columns
        checkbox_colname_maps = {}
        for map_name, map_dict in maps:
            checkbox_colname_maps[map_name] = {}
            for column in df.columns:
                if f"{map_name}___" in column:
                    prefix, suffix = column.split("___")
                    suffix = map_dict[suffix].lower().replace(" ", "-").replace(",", "").replace("(", "").replace(")", "")
                    checkbox_colname_maps[map_name][column] = f"{prefix}_{suffix}"
            if map_name in df.columns:
                df = df.drop(columns = [map_name])

        # Rename and Retype Columns
        for map_name, map_dict in checkbox_colname_maps.items():
            df = df.rename(columns = map_dict)
            for column in map_dict.values():
                df[column] = df[column].where(pd.notnull(df[column]), nonetype) # Update NaN/None/etc. to defined nonetype
                df[column] = df[column].astype(dtype) # Update to defined dtype

        return df, checkbox_colname_maps

    def __preprocess_radio_columns (self, df: pd.DataFrame, maps: list = [], dtype: typing.Any = np.float64, nonetype: typing.Any = np.nan) -> pd.DataFrame:
        """
        Pre-processing for checkbox columns
        """

        # Map Radio Columns
        radio_colname_maps = {}
        for map_name, map_dict in maps:
            radio_colname_maps[map_name] = {}
            dummies = pd.get_dummies(df[map_name], prefix = map_name)
            for column in dummies.columns:
                if f"{map_name}" in column:
                    prefix, suffix = column.split("_")
                    suffix = suffix.lower().replace(" ", "-").replace(",", "").replace("(", "").replace(")", "")
                    radio_colname_maps[map_name][column] = f"{prefix}_{suffix}"
            if map_name in df.columns:
                df = df.drop(columns = [map_name])
            df = pd.concat([df, dummies], axis = 1)

        # Rename Columns
        for map_name, map_dict in radio_colname_maps.items():
            df = df.rename(columns = map_dict)
            for column in map_dict.values():
                df[column] = df[column].where(pd.notnull(df[column]), nonetype) # Update NaN/None/etc. to defined nonetype
                df[column] = df[column].astype(dtype) # Update to defined dtype

        return df, radio_colname_maps

    def __preprocess_revalue_columns (self, df: pd.DataFrame, maps: list = []) -> typing.Tuple[pd.DataFrame, dict]:
        """
        Pre-processing for re-value columns
        """

        # Map Revalue Columns
        revalue_colname_maps = {}
        for map_name, map_dict in maps:
            revalue_colname_maps[map_name] = map_dict
            df = df.replace({map_name: map_dict})

        # Flat Merge Checkbox Column Maps
        revalue_combined_maps = {}
        for map_name, map_dict in revalue_colname_maps.items():
            revalue_combined_maps |= map_dict

        return df, revalue_combined_maps

    def __preprocess_type_columns (self, df: pd.DataFrame, columns: list, dtype: typing.Any = np.float64, nonetype: typing.Any = np.nan) -> pd.DataFrame:
        """
        Pre-processing for typing columns
        """
        df[columns] = df[columns].where(pd.notnull(df[columns]), nonetype)
        df[columns] = df[columns].astype(dtype)
        return df

    def __preprocess_remap_columns (self, df: pd.DataFrame, map: dict = {}, cols: list = []) -> pd.DataFrame:
        """
        Pre-processing column values by map
        """
        for col in cols:
            df = df.replace({col: map})

        return df

    def __preprocess_repeat_instrument_by_map (self, df: pd.DataFrame, index: list = [], repeat_instrument_maps: list = [], dtype: typing.Any = np.float32, nonetype: typing.Any = np.nan) -> pd.DataFrame:
        """
        Pre-processing REDCap repeat_instrument so each instrument has its own column and the value
        is computed using a function applied to the repeat_instance field.
        """
        # Remap repeat instruments
        for repeat_instrument_map in repeat_instrument_maps:
            df_masked = df[df["redcap_repeat_instrument"] == repeat_instrument_map["name"]]
            df_pt = pd.pivot_table(
                df_masked,
                index       = index,
                columns     = ["redcap_repeat_instrument"],
                values      = "redcap_repeat_instance",
                aggfunc     = repeat_instrument_map["aggregator"],
            )
            df = df.merge(df_pt, how = "outer", on = index)
            df = df[df["redcap_repeat_instrument"].isnull()] # Keep only rows not generated by columns

        # Rename columns
        for repeat_instrument_map in repeat_instrument_maps:
            df = df.rename(columns = {repeat_instrument_map["name"]: repeat_instrument_map["rename"]})
            df[repeat_instrument_map["rename"]] = df[repeat_instrument_map["rename"]].where(pd.notnull(df[repeat_instrument_map["rename"]]), nonetype) # Update NaN/None/etc. to defined nonetype
            df[repeat_instrument_map["rename"]] = df[repeat_instrument_map["rename"]].astype(dtype)

        # Drop repeat instrument columns
        df = df.drop(["redcap_repeat_instrument", "redcap_repeat_instance"], axis = 1)

        return df

    def __preprocess_repeat_instrument_columns (self, df: pd.DataFrame, index: list = [], aggregator: typing.Callable = np.max) -> pd.DataFrame:
        """
        Pre-processing REDCap repeat_instrument so each instrument has its own column and the value
        is computed using a function applied to the repeat_instance field.
        """
        df_pt = pd.pivot_table(
            df,
            index       = index,
            columns     = ["redcap_repeat_instrument"],
            values      = "redcap_repeat_instance",
            aggfunc     = aggregator,
        )
        df = df.merge(df_pt, how = "outer", on = index)
        df = df[df["redcap_repeat_instrument"].isnull()] # Keep only rows not generated by columns
        df = df.drop(["redcap_repeat_instrument", "redcap_repeat_instance"], axis = 1)
        return df


# DEV_SAMPLE_REPORT_DATA = os.environ["DEV_SAMPLE_REPORT_DATA"]

#
# Column Maps
#

dm_map = {
    "i": "Incomplete",
    "d": "Complete",
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

ethnic_map = {
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

combined_map = {
    **dm_map,
    **race_map,
    **ethnic_map
}

#
# Value Maps
#

binary_map = {
    "0": 0,
    "1": 1,
    "2": 2
}

redcap_repeat_instrument_variable_map = {
    "ehr_information": "EHR Information",
    "mailing_information": "Mailing Information",
    "recruitment_survey_management": "Recruitment & Survey Management",
    "recruitment_survey": "Recruitment Survey",
    "faq_survey": "FAQ Survey",
    "screening_survey": "Screening Survey",
    "screening_stop_message": "Screening Stop Message",
    "preconsent_survey": "Pre-Consent Survey",
    "consent_survey": "Consent Survey",
    "staff_consent_attestation_survey": "Staff Consent Attestation Survey",
    "download_consent": "Download Consent",
    "participant_contact_information_survey": "Participant Contact Information Survey",
    "demographics_survey": "Demographics Survey",
    "health_survey": "Health Survey",
    "substance_use_survey": "Substance Use Survey",
    "cesd10_survey": "CESD-10 Survey",
    "paid5_dm_survey": "PAID-5 Dm Survey",
    "diabetes_survey": "Diabetes Survey",
    "dietary_survey": "Dietary Survey",
    "ophthalmic_survey": "Ophthalmic Survey",
    "px_sdoh_combined_survey": "PX SDOH Combined Survey",
    "px_food_insecurity_survey": "PX Food Insecurity Survey",
    "px_neighborhood_environment_survey": "PX Neighborhood Environment Survey",
    "px_racial_ethnic_discrimination_survey": "PX Racial Ethnic Discrimination Survey",
    "decline_participation_survey": "Decline Participation Survey",
    "study_enrollment": "Study Enrollment",
    "driving_record": "Driving Record",
    "device_distribution": "Device Distribution",
    "meds_assessment": "Meds Assessment",
    "current_medications": "Current Medications",
    "physical_assessment": "Physical Assessment",
    "bcva": "BCVA",
    "photopic_mars": "Photopic Mars",
    "mesopic_mars": "Mesopic Mars",
    "monofilament": "Monofilament",
    "moca": "MoCA",
    "ecg": "ECG",
    "retinal_imaging": "Retinal Imaging",
    "lab_results": "Lab Results",
    "specimen_management": "Specimen Management",
    "device_return": "Device Return",
    "contact_log": "Contact Log",
    "disposition": "Disposition",
    "data_management": "Data Management",
}

redcap_repeat_instrument_label_map = {v: k for k, v in redcap_repeat_instrument_variable_map.items()}

#
# Computed Columns
#

dm_cols = [
    "dm_incomplete",
    "dm_complete"
]

race_cols = [
    "race_american-indian-or-alaska-native",
    "race_asian",
    "race_black-or-african-american",
    "race_middle-eastern",
    "race_native-hawaiian-or-pacific-islander",
    "race_north-african",
    "race_white-or-caucasian",
    "race_other-race-ethnicity-or-origin",
    "race_prefer-not-to-say",
]

ethnic_cols = [
    "ethnic_no",
    "ethnic_yes-mexican",
    "ethnic_yes-puerto-rican",
    "ethnic_yes-cuban",
    "ethnic_yes-dominican-republic",
    "ethnic_yes-central-american",
    "ethnic_yes-south-american",
    "ethnic_yes-chicano",
    "ethnic_yes-other",
    "ethnic_prefer-not-to-say",
]

#
# Column Groups
#

index_col = "record_id"

base_cols = [
    "siteid",
    "redcap_repeat_instrument",
    "redcap_repeat_instance",
    "redcap_data_access_group",
]

contact_cols = [
    "cnct_sccs",
    "cnct_type",
    "cnct_prp",
]

demographic_cols = [
    "genderid",
    "genderidot",
    "scrsex",
    "scrsexot",
    "raceot",
    "race2",
    "ethnicot",
    "ancestry",
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

#
# Data Frame Setup Methods
#

def __preprocess_df (df: pd.DataFrame, maps : list = []):
    """
    Generic pre-processing for all modules
    """

    # Rename Checkbox Columns
    colname_maps = {}
    for map_name, map_dict in maps:
        colname_maps[map_name] = {}
        for column in df.columns:
            if f"{map_name}___" in column:
                prefix, suffix = column.split("___")
                suffix = map_dict[suffix].lower().replace(" ", "-").replace(",", "")
                colname_maps[map_name][column] = f"{prefix}_{suffix}"

    # Flat Merge Checkbox Column Maps
    combined_maps = {}
    for map_name, map_dict in colname_maps.items():
        combined_maps |= map_dict

    # Update DataFrame
    df = df.rename(columns = combined_maps).set_index(index_col)

    return df, colname_maps

def __setup_module (module: typing.Callable, df: pd.DataFrame, cols: list = []) -> dict:
    flattened = []
    for col_group in cols:
        flattened.extend(col_group)
    return module(df, flattened)

def __get_greatest (group: pd.DataFrame, column: str) -> typing.Any:
    return group[column].max()


#
# Module Methods
#

def overview (df: pd.DataFrame, cols: list) -> dict:
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
    # overview_schema = {}
    # for i, group in df[cols].groupby(index_col):

    # # print(len(pd.unique(df.index)))
    # n = __n_participants(df)
    # print(n)
    # print(df)
    # for i, group in df[cols].groupby(index_col):
    #     if len(group) > 1:
    #         print(i, group.value_counts(ascending = True, dropna = False))
    counts = df[cols].nunique(dropna = False)
    # for key, val in zip(counts, counts.index.names):
    #     print(key, val)
    for k, v in counts.items():
        print(k, v)

    return df

def progress (df: pd.DataFrame, cols: list) -> dict:
    """
    Study protocol transform
    """
    cols = base_cols + phenotype_cols + demographic_cols + survey_cols
    return df

def demographics (df: pd.DataFrame, cols: list) -> dict:
    """
    Study demographics transform
    """
    cols = base_cols + phenotype_cols + demographic_cols
    return df

def phenotype (df: pd.DataFrame, cols: list) -> dict:
    """
    Study phenotype transform
    """
    cols = base_cols + phenotype_cols
    return df

def device (df: pd.DataFrame, cols: list) -> dict:
    """
    Study device transform
    """
    cols = base_cols + phenotype_cols + demographic_cols + device_cols
    return df

def contact (df: pd.DataFrame, cols: list) -> dict:
    """
    Study contact transform
    """
    cols = base_cols + survey_cols + device_cols + contact_cols
    return df

#
# Column Counting Methods
#

def __n_participants (df: pd.DataFrame) -> dict:
    groups = df.groupby(index_col)
    return len(groups)

if __name__ == "__main__":

    df = pd.read_csv( "../dev/data/AIREADiPilot-FairhubStudyDashboar_DATA_2023-08-08_1348.csv", sep = "\t", dtype = "str")
    df, colname_map = __preprocess_df(
        df,
        maps = [
            ("dm", dm_map),
            ("race", race_map),
            ("ethnic", ethnic_map)
        ]
    )

    overview_data = __setup_module(
        overview,
        df, [
        base_cols,
        dm_cols,
        demographic_cols,
        race_cols,
        ethnic_cols,
        phenotype_cols,
        survey_cols
    ])




