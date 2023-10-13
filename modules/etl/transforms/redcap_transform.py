# Library Modules
from typing import Any, Callable, Union, List, Dict, Tuple
import re, os, csv, json, logging

# Third Party Modules
from redcap import Project
import pandas as pd
import numpy as np


class REDCapTransform(object):
    def __init__(self, config: dict) -> None:
        #
        # Config
        #

        # REDCap API Config
        self.redcap_api_url = config["redcap_api_url"]
        self.redcap_api_key = config["redcap_api_key"]

        # Set Transform Key
        self.key = config["key"] \
            if "key" in config \
            else "redcap-transform"

        # Data Config
        self.index_columns = config["index_columns"] \
            if "index_columns" in config \
            else ["record_id"]

        # REDCap Reports Config
        self.reports_configs = config["reports"] \
            if "reports" in config \
            else []

        # Report Merging
        self.merge_transformed_reports = config["merge_transformed_reports"] \
            if "merge_transformed_reports" in config \
            else []

        # Post Merge Transforms
        self.post_merge_transforms = config["post_merge_transforms"] \
            if "post_merge_transforms" in config \
            else []

        # Column Value Separator
        self.multivalue_separator = config["multivalue_separator"] \
            if "multivalue_separator" in config \
            else "|"

        # CSV Float Format (Default: "%.2f")
        self.csv_float_format = config["csv_float_format"] \
            if "csv_float_format" in config \
            else "%.2f"

        self.missing_value_generic = config["missing_value_generic"] \
            if "missing_value_generic" in config \
            else "Value Unavailable"

        # Logging Config
        self.logging_config = config["logging_config"] \
            if "logging_config" in config \
            else {
                "encoding": "utf-8",
                "filename": "REDCapETL.log",
                "level": logging.DEBUG,
            }

        # Configure Logging
        logging.basicConfig(**self.logging_config)
        self.logger = logging.getLogger("REDCapTransform")

        #
        # REDCap Parsing Variables
        #

        # Regex Complex Field Parsers
        self._field_rgx = {}
        self._field_rgx["radio"] = re.compile(r"^[0-9\.]{1,17}")
        self._field_rgx["checkbox"] = re.compile(r"^[0-9\.]{1,17}")
        self._field_rgx["dropdown"] = re.compile(r"^[0-9\.]{1,17}")
        self._field_rgx["yesno"] = re.compile(r"^[0-9\.]{1,17}")
        self._field_rgx["text"] = re.compile(
            r"^[a-zA-Z0-9\-\_\(\)\[\]\&\+\?\!\$\*]{1,128}"
        )
        self._field_rgx["descriptive"] = re.compile(
            r"^[a-zA-Z0-9\-\_\(\)\[\]\&\+\?\!\$\*]{1,128}"
        )
        self._field_rgx["notes"] = re.compile(
            r"^[a-zA-Z0-9\-\_\(\)\[\]\&\+\?\!\$\*]{1,128}"
        )
        self._field_rgx["file"] = None
        self._field_rgx["signature"] = None
        self._field_rgx["calc"] = None

        # General Parsing Variables
        self.none_values = [np.nan, pd.NaT, None, "nan", "NaN", "-", "", self.missing_value_generic]
        self.none_map = {key: self.missing_value_generic for key in self.none_values}
        self.survey_instrument_map = {
            "2": "Complete",
            "1": "Unverified",
            "0": "Incomplete",
            "" : self.missing_value_generic
        }

        self.logger.info(f"Initialized")

        #
        # PyCap Initialization
        #

        # Initialize PyCap Objects
        self.logger.info(f"Retrieving REDCap project data")
        self.project = Project(self.redcap_api_url, self.redcap_api_key)
        self.metadata = self.project.export_metadata()
        self.repeat_events_data = self.project.export_repeating_instruments_events()

        #
        # Setup Reports & Apply Transforms
        #

        # Internal Defaults
        # - Key Assumptions for Transform Functions
        # – Only Update if REDCap API Updates
        self._reports_kwdargs = {}
        self._reports_kwdargs["raw_or_label"] = "raw"
        self._reports_kwdargs["raw_or_label_headers"] = "raw"
        self._reports_kwdargs["export_checkbox_labels"] = False
        self._reports_kwdargs["csv_delimiter"] = "\t"

        # Get & Structure Report
        self.logger.info(f"Retrieving REDCap reports")
        self.reports = {}
        for report_name, report_kwdargs, transforms in self.reports_configs:
            # Get Report
            report_kwdargs = report_kwdargs | self._reports_kwdargs
            report = self.project.export_report(**report_kwdargs)
            # Structure Reports
            self.reports[report_name] = {
                "id": report_kwdargs["report_id"],
                "report": report,
                "df": pd.DataFrame(report),
                "transforms": transforms,
                "transformed": None,
                "annotation": self._get_redcap_type_metadata(pd.DataFrame(report)),
            }

        # Generate Transformed Report
        self.logger.info(f"Applying REDCap report transforms")
        for report_name, report_object in self.reports.items():
            self._apply_report_transforms(report_name)

        # Merge Reports
        self.logger.info(f"Merging REDCap reports")
        receiving_report_name, merge_steps = self.merge_transformed_reports
        self.merged = self._merge_reports(receiving_report_name, merge_steps)

        # Apply Post-Merge Transforms
        self.logger.info(f"Applying REDCap report post-merge transforms")
        for transform, transform_kwdargs in self.post_merge_transforms:
            self.merged = self.apply_transform(
                self.merged, transform, transform_kwdargs
            )

        self.logger.info(f"REDCap transforms complete")

        return

    #
    # Getters
    #

    def get_report_id(self: object, report_name: str) -> str:
        """
        Returns a str instance of the REDCap report ID.
        """
        return self.reports[report_name]["id"]

    def get_report_pycap(
        self: object, report_name: str
    ) -> Union[List[Dict[str, Any]], str, pd.DataFrame]:
        """
        Returns a PyCap Report object containing the report.
        """
        return self.reports[report_name]["report"]

    def get_report_df(self: object, report_name: str) -> pd.DataFrame:
        """
        Returns a pd.DataFrame instance containing the report.
        """
        return self.reports[report_name]["df"]

    def get_report_transformed_df(self: object, report_name: str) -> pd.DataFrame:
        """
        Returns a pd.DataFrame instance containing the report
        with normalization transforms applied.
        """
        return self.reports[report_name]["transformed"]

    def get_report_transforms(
        self: object, report_name: str
    ) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Returns a list of transforms that will be applied to
        the report
        """
        return self.reports[report_name]["transforms"]

    def get_report_annotations(self: object, report_name: str) -> List[Dict[str, Any]]:
        """
        Returns a list of annotations generated from the
        REDCap metadata API call.
        """
        return self.reports[report_name]["annotations"]

    #
    # Transform Applicator
    #

    # Applies Declared Transforms to Reports
    def _apply_report_transforms(self: object, report_name: str) -> None:
        """
        Interal method that applies the transforms to each
        report as an idempotent transform stack.
        """
        report = self.reports[report_name]
        annotation = report["annotation"]
        report["transformed"] = report["df"]
        for transform in report["transforms"]:
            transform_name, transform_kwdargs = transform
            transform_kwdargs = transform_kwdargs | {"annotation": annotation}
            report["transformed"] = self.apply_transform(
                report["transformed"], transform_name, transform_kwdargs
            )

        return self

    def apply_transform(
        self: object,
        df: pd.DataFrame,
        transform_name: str,
        transform_kwdargs: Dict[str, Any] = {},
    ) -> pd.DataFrame:
        return getattr(self, f"_{transform_name}")(df, **transform_kwdargs)

    #
    # Transforms - Columns
    #

    #
    # Drop Columns
    #

    def _drop_columns(
        self: object,
        df: pd.DataFrame,
        columns: List[str] = [],
        annotation: List[Dict[str, Any]] = [],
    ) -> pd.DataFrame:
        columns = self._resolve_columns_with_dataframe(df=df, columns=columns)
        df = df.drop(columns=columns)
        return df

    @classmethod
    def drop_columns(
        self: object, df: pd.DataFrame, columns: List[str]
    ) -> pd.DataFrame:
        """
        Drop columns from pd.DataFrame.
        """
        return self._drop_columns(df=df, columns=columns)

    #
    # Keep Columns
    #

    def _keep_columns(
        self: object,
        df: pd.DataFrame,
        columns: List[str] = [],
        annotation: List[Dict[str, Any]] = [],
    ) -> pd.DataFrame:
        columns = set(df.columns) - set(
            self._resolve_columns_with_dataframe(df=df, columns=columns)
        )
        df = df.drop(columns=columns)
        return df

    @classmethod
    def keep_columns(
        self: object, df: pd.DataFrame, columns: List[str]
    ) -> pd.DataFrame:
        """
        Keep only selected columns in pd.DataFrame.
        """
        return self._keep_columns(df=df, columns=columns)

    #
    # Transform - Append Column Prefix
    #

    def _append_column_suffix(
        self: object,
        df: pd.DataFrame,
        columns: List[str] = [],
        suffix: str = "",
        separator: str = "",
        annotation: List[Dict[str, Any]] = [],
    ) -> pd.DataFrame:
        columns = self._resolve_columns_with_dataframe(df=df, columns=columns)
        df[columns] = df[columns].rename(
            mapper=lambda name: f"{namer}{separator}{suffix}"
        )
        return df

    @classmethod
    def append_column_suffix(
        self: object,
        df: pd.DataFrame,
        columns: List[str] = [],
        suffix: str = "",
        separator: str = "",
    ) -> pd.DataFrame:
        """
        Append a suffix to columns of pd.DataFrame. Note: If no
        columns parameter is provided, the suffix is applied every
        column. If no suffix is provided, the column names remain
        unchanged. A separator argument allows for the expansion
        of column names by one or more characters, e.g. "_" for
        snakecase.
        """
        return self._prepend_column_suffix(
            df=df, columns=transform_columns, suffix=suffix, separator=separator
        )

    #
    # Transform - Prepend Column Prefix
    #

    def _prepend_column_prefix(
        self: object,
        df: pd.DataFrame,
        columns: List[str] = [],
        prefix: str = "",
        separator: str = "",
        annotation: List[Dict[str, Any]] = [],
    ) -> pd.DataFrame:
        columns = self._resolve_columns_with_dataframe(df=df, columns=columns)
        df[columns] = df[columns].rename(
            mapper=lambda name: f"{prefix}{separator}{name}"
        )
        return df

    @classmethod
    def prepend_column_prefix(
        self: object,
        df: pd.DataFrame,
        columns: List[str] = [],
        prefix: str = "",
        separator: str = "",
    ) -> pd.DataFrame:
        """
        Append a prefix to columns of pd.DataFrame. Note: If no
        columns parameter is provided, the prefix is applied every
        column. If no prefix is provided, the column names remain
        unchanged. A separator argument allows for the expansion
        of column names by one or more characters, e.g. "_" for
        snakecase.
        """
        return self._prepend_column_prefix(
            df=df, columns=columns, prefix=prefix, separator=separator
        )

    #
    # Transforms - Remap Values by Columns
    #

    def _remap_values_by_columns(
        self: object,
        df: pd.DataFrame,
        columns: List[str],
        value_map: Dict[str, Any] = {},
        annotation: List[Dict[str, Any]] = [],
    ) -> pd.DataFrame:
        # Resolve Mappable Fields and Available Value Maps
        columns = self._resolve_columns_with_dataframe(df=df, columns=columns)

        if len(value_map) > 0:
            mappable_fields = [
                {"name": column, "options": value_map} for column in columns
            ]
        else:
            mappable_fields = [
                field
                for field in annotation
                if field["options"] is not None and field["name"] in columns
            ]

        for mappable_field in mappable_fields:
            column, value_map = mappable_field["name"], mappable_field["options"]
            for i, value in enumerate(df[column]):
                subvalues = [
                    subvalue.strip()
                    for subvalue in str(value).split(",")
                    if len(subvalue) > 0
                ]
                df[column][i] = self.multivalue_separator.join(
                    [
                        value_map[subvalue]
                        for subvalue in subvalues
                        if subvalue in value_map.keys()
                    ]
                )

        return df

    @classmethod
    def remap_values_by_columns(
        self: object,
        df: pd.DataFrame,
        columns: List[str],
        value_map: Dict[str, Any] = {},
    ) -> pd.DataFrame:
        """
        Remap values by column using a list of annotations.
        Each annotation is a dictionary containing a the
        following keys: "name", "type", and "options". Key
        to this method are then "name" and "options" entries.
        The value of the "name" corresponds to the
        pd.DataFrame column name. The value of the"options"
        entry is a value_map object generated from the
        REDCapo metadata API request:

        annotation = {
            "name": field["field_name"],
            "type": field["field_type"],
            "options": field["field_options"]
        }

        If multiple values are found in the field, they will
        be mapped with a separator. The default separator is
        a pipe (i.e. "|").

        Returns a transformed pd.DataFrame
        """
        return self._remap_values_by_columns(
            df=df, columns=columns, value_map=value_map
        )

    #
    # Transform - Map Missing Values By Columns
    #

    def _map_missing_values_by_columns (self: object, df: pd.DataFrame, columns: List[str], missing_value: Any = None, annotation: List[Dict[str, Any]] = []) -> pd.DataFrame:
        columns = self._resolve_columns_with_dataframe(df = df, columns = columns)
        missing_value = missing_value if missing_value is not None else self.missing_value_generic
        for column in columns:
            for i, value in enumerate(df[column]):
                if (len(str(value)) == 0) or (value in self.none_map.keys()):
                    df[column][i] = missing_value
                else:
                    continue

        return df

    @classmethod
    def map_missing_values_by_columns (self: object, df: pd.DataFrame, columns: List[str], missing_value: Any) -> pd.DataFrame:
        """
        Replace 0-length values or values with keys in
        self.none_map with self.missing_value_generic.
        """
        return self._map_missing_values_by_columns(df = df, columns = columns, missing_value = missing_value)

    #
    # Transforms - Rows
    #

    #
    # Drop Rows
    #

    def _drop_rows(
        self: object,
        df: pd.DataFrame,
        columns: List[str] = [],
        condition: Callable = lambda column: column == "",
        annotation: List[Dict[str, Any]] = [],
    ) -> pd.DataFrame:
        columns = self._resolve_columns_with_dataframe(df=df, columns=columns)
        df = df[~df[columns].apply(lambda column: column.apply(condition)).any(axis=1)]
        return df

    @classmethod
    def drop_rows(
        self: object,
        df: pd.DataFrame,
        columns: List[str],
        condition: Callable = lambda column: column == "",
    ) -> pd.DataFrame:
        """
        Drop rows from pd.DataFrame.
        """
        return self._drop_rows(df=df, columns=columns)

    #
    # Transforms - Aggregation
    #

    #
    # Transforms - Aggregate Repeat Instruments by Index
    #

    def _aggregate_repeat_instrument_column_by_index (self: object, df: pd.DataFrame, aggregator: str = "max", dtype: Callable = float, annotation: List[Dict[str, Any]] = []) -> pd.DataFrame:
        new_columns = df["redcap_repeat_instrument"].unique()
        pivot = pd.pivot_table(
            df,
            index       = self.index_columns,
            columns     = ["redcap_repeat_instrument"],
            values      = "redcap_repeat_instance",
            aggfunc     = aggregator,
            fill_value  = self.missing_value_generic
        )
        df = df.merge(pivot, how="inner", on=self.index_columns)
        df = df.drop_duplicates(self.index_columns, keep="first")
        for column in new_columns:
            df[column] = df[column].astype(dtype)
        return df

    @classmethod
    def aggregate_repeat_instrument_by_index (self: object, df: pd.DataFrame, aggregator: str = "max", dtype: Callable = float) -> pd.DataFrame:
        """
        Pre-processing REDCap repeat_instrument so each instrument
        has its own column and the value. The value is computed
        using an aggregation function applied to the repeat_instance
        field.
        """
        return self._aggregate_repreat_instrument_by_index(
            df=df, aggregator=aggregator, dtype=dtype
        )

    #
    # Report Merging
    #

    def _merge_reports(
        self: object,
        receiving_report_name: str,
        merge_steps: List[Tuple[str, Dict[str, Any]]],
    ) -> pd.DataFrame:
        """
        Performns N - 1 merge transforms on N reports.
        """

        df_receiving_report = self.reports[receiving_report_name]["transformed"]

        if len(merge_steps) > 0:
            for providing_report_name, merge_kwdargs in merge_steps:
                df_providing_report = self.reports[providing_report_name]["transformed"]
                df_receiving_report = df_receiving_report.merge(
                    df_providing_report, **merge_kwdargs
                )
        else:
            self.logger.warn(
                f"Unable to Merge – No merge steps provided, returning receiving_report pd.DataFrame."
            )

        return df_receiving_report

    #
    # Utilities
    #

    # Transform Prelude - Get Applicable Transform Columns
    def _resolve_columns_with_dataframe(
        self: object, df: pd.DataFrame, columns: List[str]
    ) -> List[str]:
        """
        Internal utility function. Uses set logic to ensure
        requested columns are available within the target
        pd.DataFrame.
        """
        available_columns, requested_columns = set(df.columns), set(columns)
        resolved_columns = []

        if len(requested_columns) == 0:
            self.logger.warn(
                f"Unexpected Transform – columns parameter has no values. Defaulting to df.columns"
            )
            resolved_columns = [*available_columns]
        elif len(available_columns & requested_columns) == 0:
            self.logger.warn(
                f"Unexpected Transform – none of the values in the columns parameter were found in df.columns. Defaulting to df.columns"
            )
            resolved_columns = [*available_columns]
        elif len(requested_columns - available_columns) > 0:
            self.logger.warn(
                f"Unexpected Transform – df.columns missing values present in columns parameter: {', '.join([*requested_columns - available_columns])}. Continuing with union."
            )
            resolved_columns = [*(available_columns & requested_columns)]
        else:
            resolved_columns = [*requested_columns]

        return resolved_columns

    #  Extract REDCap Type Metadata
    def _get_redcap_type_metadata(
        self: object, df: pd.DataFrame
    ) -> List[Dict[str, Any]]:
        """
        Extracts REDCap field name, type, and options (the
        metadata) for each column in the target pd.DataFrame
        """

        # REDCap Internal Variable Metadata
        metadata = [
            {"name": "redcap_data_access_group", "type": "text", "options": None},
            {"name": "redcap_repeat_instrument", "type": "text", "options": None},
            {"name": "redcap_repeat_instance", "type": "number", "options": None},
        ]

        field_types = set(field["field_type"] for field in self.metadata)
        complex_types = {"dropdown", "radio", "checkbox"}
        binary_types = {"yesno"}
        text_types = {"text"}
        skip_types = {"file", "calc", "descriptive", "notes"}

        # Get Column Metadata
        columns = df.columns.tolist()
        for field in sorted(self.metadata, key=lambda f: f["field_name"]):
            if field["field_name"] in columns:
                field_type = field["field_type"]
                options = {}
                if field_type in complex_types:
                    rgx = self._field_rgx[field_type]
                    for option in field["select_choices_or_calculations"].split("|"):
                        k, v = (
                            option.split(",")[0],
                            (",".join(option.split(",")[1:])).strip(),
                        )
                        k = int(k) if re.match(rgx, k) else str(k)
                        v = int(v) if re.match(rgx, v) else str(v)
                        options[str(k)] = v
                    metadata.append(
                        {
                            "name": field["field_name"],
                            "type": field["field_type"],
                            "options": options | self.none_map,
                        }
                    )
                elif field_type in binary_types:
                    metadata.append(
                        {
                            "name": field["field_name"],
                            "type": field["field_type"],
                            "options": {"1": "Yes", "0": "No"} | self.none_map,
                        }
                    )
                elif field_type in text_types:
                    metadata.append(
                        {
                            "name": field["field_name"],
                            "type": field["field_type"],
                            "options": None,
                        }
                    )
                elif field_type in skip_types:
                    metadata.append(
                        {
                            "name": field["field_name"],
                            "type": field["field_type"],
                            "options": None,
                        }
                    )
                else:
                    continue

        return metadata

    #
    # Exports
    #

    # Export Untransformed (Raw) Reports
    def export_raw(
        self: object, path: str = "", separator: str = "\t", filetype: str = ".tsv"
    ) -> object:
        for report_name, report_object in self.reports.items():
            filename = f"{report_name}_raw{filetype}"
            filepath = os.path.join(path, filename)
            transformed = report_object["df"]
            transformed.to_csv(
                filepath,
                sep=separator,
                quoting=csv.QUOTE_NONNUMERIC,
                float_format=self.csv_float_format,
            )
        return self

    # Export Transformed Reports
    def export_transformed(
        self: object, path: str = "", separator: str = "\t", filetype: str = ".tsv"
    ) -> object:
        for report_name, report_object in self.reports.items():
            filename = f"{report_name}_transformed{filetype}"
            filepath = os.path.join(path, filename)
            transformed = report_object["transformed"]
            transformed.to_csv(
                filepath,
                sep=separator,
                quoting=csv.QUOTE_NONNUMERIC,
                float_format=self.csv_float_format,
            )
        return self

    # Export Merged Transforms
    def export_merged_transformed(
        self: object, path: str = "", separator: str = "\t", filetype: str = ".tsv"
    ) -> object:
        filename = f"transformed-merged_redcap-extract{filetype}"
        filepath = os.path.join(path, filename)
        self.merged.to_csv(
            filepath,
            sep=separator,
            quoting=csv.QUOTE_NONNUMERIC,
            float_format=self.csv_float_format,
        )
        return self


if __name__ == "__main__":
    pass
else:
    pass
