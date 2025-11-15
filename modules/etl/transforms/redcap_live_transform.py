# Library Modules
from typing import Any, Callable, Union, List, Dict, Tuple, Literal
import re, os, logging, copy

# Third Party Modules
from redcap import Project
import polars as pl
import numpy as np

class RedcapLiveTransform(object):
    def __init__(self, config: dict):

        #
        # Config
        #

        #
        self.config = copy.deepcopy(config)

        # Get CWD
        self.cwd = os.getcwd()

        # REDCap API Config
        self.redcap_api_url = self.config["redcap_api_url"]
        self.redcap_api_key = self.config["redcap_api_key"]

        # Data Config
        self.index_columns = (
            self.config["index_columns"] if "index_columns" in self.config else ["record_id"]
        )

        # REDCap Reports Config
        self.reports_configs = self.config["reports"] if "reports" in self.config else []

        # Report Merging
        self.post_transform_merge = (
            self.config["post_transform_merge"]
            if "post_transform_merge" in self.config
            else ([], [])
        )

        # Post Merge Transforms
        self.post_merge_transforms = (
            self.config["post_merge_transforms"] if "post_merge_transforms" in self.config else []
        )

        # Column Value Separator
        self.multivalue_separator = (
            self.config["multivalue_separator"] if "multivalue_separator" in self.config else "|"
        )

        # CSV Float Format (Default: "%.2f")
        self.csv_float_format = (
            self.config["csv_float_format"] if "csv_float_format" in self.config else "%.2f"
        )

        self.missing_value_generic = (
            self.config["missing_value_generic"]
            if "missing_value_generic" in self.config
            else "Value Unavailable"
        )

        # Logging Config
        self.logging_config = (
            self.config["logging_config"]
            if "logging_config" in self.config
            else {
                "encoding": "utf-8",
                "filename": "REDCapETL.log",
                "level": logging.INFO,
            }
        )

        # Configure Logging
        logging.basicConfig(**self.logging_config)
        self.logger = logging.getLogger("RedcapTransform:Live")

        #
        # REDCap Parsing Variables
        #

        # Regex Complex Field Parsers
        self._field_rgx = {
            "radio": re.compile(r"^[0-9\.]{1,17}"),
            "checkbox": re.compile(r"^[0-9\.]{1,17}"),
            "dropdown": re.compile(r"^[0-9\.]{1,17}"),
            "yesno": re.compile(r"^[0-9\.]{1,17}"),
            "text": re.compile(r"^[a-zA-Z0-9\-\_\(\)\[\]\&\+\?\!\$\*]{1,128}"),
            "descriptive": re.compile(r"^[a-zA-Z0-9\-\_\(\)\[\]\&\+\?\!\$\*]{1,128}"),
            "notes": re.compile(r"^[a-zA-Z0-9\-\_\(\)\[\]\&\+\?\!\$\*]{1,128}"),
            "file": re.compile(r".*"),
            "signature": re.compile(r".*"),
            "calc": re.compile(r".*"),
        }

        # General Parsing Variables
        # Note: Polars handles nulls differently (null vs NaN).
        # We map standard "empty" markers to the generic missing value.
        self.none_values = [
            np.nan,
            None,
            "nan",
            "NaN",
            "-",
            "",
            self.missing_value_generic,
        ]
        self.none_map = {key: self.missing_value_generic for key in self.none_values}

        self.logger.info(f"Initialized")

        #
        # Setup Reports & Apply Transforms
        #

        # Internal Defaults
        # - Key Assumptions for Transform Functions
        # – Only Update if REDCap API and/or PyCap Update
        self._default_report_kwdargs = {
            "raw_or_label": "raw",
            "raw_or_label_headers": "raw",
            "export_checkbox_labels": False,
            "csv_delimiter": ",",
        }

        self.project: Any = None
        self.reports: Dict[str, Any] = {}
        self.merged: pl.DataFrame = pl.DataFrame([])

    def run(self):
        """
        Execute ETL
        """

        #
        # PyCap Initialization
        #

        # Initialize PyCap Objects
        self.logger.info(f"Retrieving REDCap project data")
        self.project = Project(self.redcap_api_url, self.redcap_api_key)

        # Load REDCap Project Metadata
        self.metadata: Any = self.project.export_metadata()

        self.logger.info(f"Retrieving Live REDCap reports")
        for report_config in self.reports_configs:
            # Get Report
            report_key = report_config["key"]
            report_kwdargs = report_config["kwdargs"] | self._default_report_kwdargs
            report_transforms = report_config["transforms"]

            # PyCap returns a list of dicts by default.
            report_data: Any = self.project.export_report(**report_kwdargs)

            # Convert to Polars ensuring all columns are input as UTF8 Strings
            if not report_data:
                df = pl.DataFrame([])
            else:
                # Calculate schema to force Utf8 to prevent type inference issues on ragged data
                schema = {key: pl.Utf8 for key in set().union(*(d.keys() for d in report_data))}
                df = pl.from_dicts(report_data, schema=schema)

            # Structure Reports
            self.reports[report_key] = {
                "id": report_kwdargs["report_id"],
                "df": df.rechunk(),
                "transforms": report_transforms,
                "transformed": None,
                "annotation": self._get_redcap_type_metadata(df),
            }

        try:

            # Apply Pre-Merge Report Transforms
            self.logger.info(f"Applying REDCap report transforms")
            for report_key, report_object in self.reports.items():
                self._apply_report_transforms(report_key)

            # Merge Reports
            self.logger.info(f"Merging REDCap reports")
            index_columns, merge_steps = self.post_transform_merge
            self.merged = self._merge_reports(index_columns, merge_steps)

            # Apply Post-Merge Transforms
            self.logger.info(f"Applying REDCap report post-merge transforms")
            for transform, transform_kwdargs in self.post_merge_transforms:
                self.merged = self.apply_transform(
                    self.merged, transform, transform_kwdargs
                )

            self.logger.info(f"REDCap transforms complete")

        except Exception as error:
            self.logger.error(error)
            self.logger.error("An error occurred during REDCap ETL. See above stacktrace.")

        return self

    #
    # Getters
    #

    def get_report_id(self, report_key: str) -> str:
        return self.reports[report_key]["id"]

    def get_report_df(self, report_key: str) -> pl.DataFrame:
        return self.reports[report_key]["df"]

    def get_report_transformed_df(self, report_key: str) -> pl.DataFrame:
        return self.reports[report_key]["transformed"]

    def get_report_transforms(
        self, report_key: str
    ) -> List[Tuple[str, Dict[str, Any]]]:
        return self.reports[report_key]["transforms"]

    def get_report_annotations(self, report_key: str) -> List[Dict[str, Any]]:
        return self.reports[report_key]["annotations"]

    #
    # Report Merging
    #

    def _merge_reports(
        self,
        index_columns: List[str],
        merge_steps: List[Tuple[str, Dict[str, Any]]],
    ) -> pl.DataFrame:

        receiving_report_key, _ = merge_steps[0]
        df_receiving_report = self.reports[receiving_report_key]["transformed"].select(
            index_columns
        )

        if len(merge_steps) > 0:
            for merge_step in merge_steps:
                providing_report_key, merge_kwdargs = merge_step
                df_providing_report = self.reports[providing_report_key]["transformed"]

                # Map Pandas merge args to Polars join args
                how = merge_kwdargs.get("how", "inner")

                # Handle on/left_on/right_on
                on = merge_kwdargs.get("on", None)
                left_on = merge_kwdargs.get("left_on", None)
                right_on = merge_kwdargs.get("right_on", None)

                if not on and not left_on:
                    on = index_columns
                df_receiving_report, df_providing_report = df_receiving_report.rechunk(), df_providing_report.rechunk()
                df_receiving_report = df_receiving_report.join(
                    df_providing_report,
                    on=on,
                    left_on=left_on,
                    right_on=right_on,
                    how=how,
                    suffix=merge_kwdargs.get("suffixes", ("_x", "_y"))[1]
                    if "suffixes" in merge_kwdargs else "_right"
                )
        else:
            self.logger.warn(
                f"Unable to Merge – No merge steps provided, returning receiving_report pl.DataFrame."
            )

        return df_receiving_report

    #
    # Transform Applicator
    #

    def _apply_report_transforms(self, report_key: str) -> None:
        report = self.reports[report_key]
        annotation = report["annotation"]
        # Clone to avoid mutating original reference
        report["transformed"] = report["df"].clone()
        for transform in report["transforms"]:
            transform_name, transform_kwdargs = transform
            transform_kwdargs = transform_kwdargs | {"annotation": annotation}
            report["transformed"] = self.apply_transform(
                report["transformed"], transform_name, transform_kwdargs
            )
        return

    def apply_transform(
        self,
        df: pl.DataFrame,
        transform_name: str,
        transform_kwdargs: Dict[str, Any] = {},
    ) -> pl.DataFrame:
        return getattr(self, f"_{transform_name}")(df, **transform_kwdargs)

    #
    # Transforms - Columns
    #

    #
    # Drop Columns
    #

    def _drop_columns(
        self,
        df: pl.DataFrame,
        columns: List[str] = [],
        annotation: List[Dict[str, Any]] = [],
    ) -> pl.DataFrame:
        columns = self._resolve_columns_with_dataframe(df=df, columns=columns, default_columns=[])
        if columns:
            df = df.drop(columns)
        return df

    def drop_columns(self, df: pl.DataFrame, columns: List[str]) -> pl.DataFrame:
        return self._drop_columns(df=df, columns=columns)

    #
    # Keep Columns
    #

    def _keep_columns(
        self,
        df: pl.DataFrame,
        columns: List[str] = [],
        annotation: List[Dict[str, Any]] = [],
    ) -> pl.DataFrame:
        columns = self._resolve_columns_with_dataframe(df=df, columns=columns, default_columns=df.columns)
        df = df.select(columns)
        return df

    def keep_columns(self, df: pl.DataFrame, columns: List[str]) -> pl.DataFrame:
        return self._keep_columns(df=df, columns=columns)

    #
    # Transform - Append Column Prefix
    #

    def _append_column_suffix(
        self,
        df: pl.DataFrame,
        columns: List[str] = [],
        suffix: str = "",
        separator: str = "",
        annotation: List[Dict[str, Any]] = [],
    ) -> pl.DataFrame:
        columns = self._resolve_columns_with_dataframe(df=df, columns=columns, default_columns=[])
        rename_map = {col: f"{col}{separator}{suffix}" for col in columns}
        df = df.rename(rename_map)
        return df

    def append_column_suffix(
        self,
        df: pl.DataFrame,
        columns: List[str] = [],
        suffix: str = "",
        separator: str = "",
    ) -> pl.DataFrame:
        return self._append_column_suffix(
            df=df, columns=columns, suffix=suffix, separator=separator
        )

    #
    # Transform - Prepend Column Prefix
    #

    def _prepend_column_prefix(
        self,
        df: pl.DataFrame,
        columns: List[str] = [],
        prefix: str = "",
        separator: str = "",
        annotation: List[Dict[str, Any]] = [],
    ) -> pl.DataFrame:
        columns = self._resolve_columns_with_dataframe(df=df, columns=columns, default_columns=[])
        rename_map = {col: f"{prefix}{separator}{col}" for col in columns}
        df = df.rename(rename_map)
        return df

    def prepend_column_prefix(
        self,
        df: pl.DataFrame,
        columns: List[str] = [],
        prefix: str = "",
        separator: str = "",
    ) -> pl.DataFrame:
        return self._prepend_column_prefix(
            df=df, columns=columns, prefix=prefix, separator=separator
        )

    #
    # Transforms - Remap Values by Columns
    #

    def _remap_values_by_columns(
        self,
        df: pl.DataFrame,
        columns: List[str],
        value_map: Dict[str, Any] = {},
        annotation: List[Dict[str, Any]] = [],
    ) -> pl.DataFrame:
        # Resolve Mappable Fields
        columns = self._resolve_columns_with_dataframe(df=df, columns=columns, default_columns=[])

        mappable_fields: List[Dict[str, Any]]
        if len(value_map) > 0:
            mappable_fields = [
                {"name": column, "options": value_map} for column in columns
            ]
        else:
            mappable_fields = [
                field
                for field in annotation
                if len(field["options"]) > 0 and field["name"] in columns
            ]

        # Vectorized Re-mapping
        expressions = []

        for mappable_field in mappable_fields:
            column_name = mappable_field["name"]
            mapping_options = mappable_field["options"]

            # Ensure keys in mapping are strings for replacement
            str_mapping = {str(k): str(v) for k, v in mapping_options.items()}

            # 1. Split string by comma (handling potential multivalue fields)
            # 2. Replace values in the list using the mapping (default to original if not found)
            # 3. Join back with the configured separator
            expr = (
                pl.col(column_name)
                .cast(pl.Utf8) # Ensure string for splitting
                .str.split(",")
                .list.eval(
                    pl.element()
                    .str.strip_chars() # Strip whitespace from CSV parsing "1, 2" -> "2"
                    .replace(str_mapping, default=pl.element())
                )
                .list.join(self.multivalue_separator)
                .alias(column_name)
            )
            expressions.append(expr)

        if expressions:
            df = df.with_columns(expressions)

        return df

    def remap_values_by_columns(
        self,
        df: pl.DataFrame,
        columns: List[str],
        value_map: Dict[str, Any] = {},
    ) -> pl.DataFrame:
        return self._remap_values_by_columns(
            df=df, columns=columns, value_map=value_map
        )

    #
    # Transform - Values By Column
    #

    def _transform_values_by_column(
        self,
        df: pl.DataFrame,
        column: str,
        new_column_name: str,
        transform: Callable,
        missing_value: Any,
        annotation: List[Dict[str, Any]] = [],
    ) -> pl.DataFrame:
        # In Polars, using an arbitrary python callable (lambda) via map_elements
        # is the equivalent of pandas apply.

        # FIX: The user's transform lambda (e.g., date functions) might return Integers/Floats.
        # Polars map_elements with return_dtype=pl.Utf8 strictly enforces string returns.
        # We wrap the transform in a helper that forces string conversion before returning to Polars.

        def safe_string_transform(val):
            # If the value coming in is our known missing value, return it immediately
            if val == str(missing_value):
                return str(missing_value)
            try:
                # Apply user transform
                result = transform(val)
                # Force cast to string to satisfy pl.Utf8 return type
                return str(result) if result is not None else str(missing_value)
            except Exception:
                # If transformation fails (e.g. date parse error), return missing value
                return str(missing_value)

        df = df.with_columns(
            pl.when(pl.col(column) != str(missing_value))
            .then(
                pl.col(column).map_elements(safe_string_transform, return_dtype=pl.Utf8)
            )
            .otherwise(pl.lit(str(missing_value)))
            .alias(new_column_name)
        )

        # Ensure no actual nulls slip through
        df = df.with_columns(pl.col(new_column_name).fill_null(str(missing_value)))

        return df

    def transform_values_by_column(
        self,
        df: pl.DataFrame,
        column: str,
        new_column_name: str,
        transform: Callable,
        missing_value: Any,
    ) -> pl.DataFrame:
        return self._transform_values_by_column(
            df=df,
            column=column,
            new_column_name=new_column_name,
            transform=transform,
            missing_value=missing_value,
        )

    #
    # Transform - Map Missing Values By Columns
    #

    def _map_missing_values_by_columns(
        self,
        df: pl.DataFrame,
        columns: List[str],
        missing_value: Any = None,
        annotation: List[Dict[str, Any]] = [],
    ) -> pl.DataFrame:
        columns = self._resolve_columns_with_dataframe(df=df, columns=columns, default_columns=[])
        missing_value = (
            missing_value if missing_value is not None else self.missing_value_generic
        )

        # Vectorized update
        expressions = []
        none_keys = list(self.none_map.keys())

        for col_name in columns:
            # Check for null, empty string, or "nan"/"NaN" string matches
            is_missing = (
                pl.col(col_name).is_null() |
                (pl.col(col_name) == "") |
                (pl.col(col_name).is_in([str(k) for k in none_keys]))
            )

            expr = (
                pl.when(is_missing)
                .then(pl.lit(str(missing_value))) # Ensure literal is string
                .otherwise(pl.col(col_name))
                .alias(col_name)
            )
            expressions.append(expr)

        if expressions:
            df = df.with_columns(expressions)

        return df

    def map_missing_values_by_columns(
        self, df: pl.DataFrame, columns: List[str], missing_value: Any
    ) -> pl.DataFrame:
        return self._map_missing_values_by_columns(
            df=df, columns=columns, missing_value=missing_value
        )

    #
    # Transforms - Rows
    #

    #
    # Drop Rows
    #

    def _drop_rows(
        self,
        df: pl.DataFrame,
        columns: List[str] = [],
        condition: Callable[[str], pl.Expr] = lambda col_name: pl.col(col_name) == "",
        annotation: List[Dict[str, Any]] = [],
    ) -> pl.DataFrame:

        columns = self._resolve_columns_with_dataframe(df=df, columns=columns, default_columns=[])
        if not columns:
            return df
        expressions = [condition(col) for col in columns]
        mask = pl.any_horizontal(expressions).fill_null(False)
        df = df.filter(~mask)

        return df

    def drop_rows(
        self,
        df: pl.DataFrame,
        columns: List[str],
        condition: Callable[[str], pl.Expr] = lambda col_name: pl.col(col_name) == "",
    ) -> pl.DataFrame:
        return self._drop_rows(df=df, columns=columns, condition=condition)

    #
    # Transforms - Aggregation
    #

    #
    # Transforms - Aggregate Repeat Instruments by Index
    #

    def _aggregate_repeat_instrument_by_index(
        self,
        df: pl.DataFrame,
        aggregator: Literal['min', 'max', 'first', 'last', 'sum', 'mean', 'median', 'len'] | pl.Expr | None = "max",
        dtype: Callable = float,
        annotation: List[Dict[str, Any]] = [],
    ) -> pl.DataFrame:

        # Check if repeat instrument exists
        if "redcap_repeat_instrument" not in df.columns:
             return df

        df = df.filter(
            pl.col("redcap_repeat_instrument").is_not_null() &
            pl.all_horizontal(pl.col(c).is_not_null() for c in self.index_columns)
        )

        # Create the pivoted dataframe
        df = df.rechunk() # Avoid Polars/Rust race condition
        pivot_df = df.pivot(
            values="redcap_repeat_instance",
            index=self.index_columns,
            on="redcap_repeat_instrument",
            aggregate_function=aggregator
        )

        # The pivot might introduce nulls, fill with missing generic
        pivot_df = pivot_df.fill_null(self.missing_value_generic)

        # Merge back to original (outer join)
        df_unique = df.unique(subset=self.index_columns, keep="first")
        df_unique.rechunk()
        df = df_unique.join(pivot_df, on=self.index_columns, how="left")

        # Cast new columns (all columns in pivot_df except index)
        new_columns = [c for c in pivot_df.columns if c not in self.index_columns]

        # Map python types to Polars types
        pl_type = pl.Float64 if dtype is float else pl.Int64 if dtype is int else pl.Utf8
        if dtype is int: pl_type = pl.Int64

        for column in new_columns:
            df = df.with_columns(
                pl.when(pl.col(column) == self.missing_value_generic)
                .then(None)
                .otherwise(pl.col(column))
                .cast(pl_type, strict=False)
                .alias(column)
            )

        return df

    def aggregate_repeat_instrument_by_index(
        self, df: pl.DataFrame, aggregator: Literal['min', 'max', 'first', 'last', 'sum', 'mean', 'median', 'len'] | pl.Expr | None = "max", dtype: Callable = float
    ) -> pl.DataFrame:
        return self._aggregate_repeat_instrument_by_index(
            df=df, aggregator=aggregator, dtype=dtype
        )

    #
    # Generate New Columns
    #

    def _new_column_from_binary_columns_positive_class(
        self,
        df: pl.DataFrame,
        column_name_map: dict,
        new_column_name: str = "",
        all_negative_value: str = "",
        default_value: str | None = "Value Unavailable",
        dtype: Callable = float,
        annotation: List[Dict[str, Any]] = [],
    ) -> pl.DataFrame:
        new_column_name = (
            new_column_name
            if len(new_column_name) > 0
            else "_".join(column_name_map.keys())
        )

        # Build a list of expressions: If Col == Yes then "Label|" else ""
        concat_exprs = []
        for col_name, label in column_name_map.items():
            concat_exprs.append(
                pl.when(pl.col(col_name) == "Yes")
                .then(pl.lit(f"{label}{self.multivalue_separator}"))
                .otherwise(pl.lit(""))
            )

        # Concatenate them all
        full_str_col = pl.concat_str(concat_exprs)

        # Check for default value presence
        any_default = pl.any_horizontal([
            pl.col(c) == default_value for c in column_name_map.keys()
        ])

        df = df.with_columns(
            pl.when((full_str_col == "") & any_default)
            .then(pl.lit(default_value))
            .when(full_str_col == "")
            .then(pl.lit(all_negative_value))
            .otherwise(
                # Remove trailing separator
                full_str_col.str.strip_chars_end(self.multivalue_separator)
            )
            .alias(new_column_name)
        )

        return df

    def new_column_from_binary_columns_positive_class(
        self,
        df: pl.DataFrame,
        column_name_map: dict,
        new_column_name: str = "",
        all_negative_value: str = "",
        default_value: str | None = "Value Unavailable",
        dtype: Callable = float,
    ) -> pl.DataFrame:
        return self._new_column_from_binary_columns_positive_class(
            df=df,
            column_name_map=column_name_map,
            new_column_name=new_column_name,
            all_negative_value=all_negative_value,
            default_value=default_value,
            dtype=dtype,
        )

    def _new_column_from_binary_columns_negative_class(
        self,
        df: pl.DataFrame,
        column_name_map: dict,
        new_column_name: str = "",
        dtype: Callable = float,
    ) -> pl.DataFrame:
        new_column_name = (
            new_column_name
            if len(new_column_name) > 0
            else "_".join(column_name_map.keys())
        )

        target_cols = list(column_name_map.keys())
        idx_to_col = {i: name for i, name in enumerate(target_cols)}

        df = df.with_columns(
            pl.concat_list([
                pl.col(c).cast(pl.Float64, strict=False) for c in target_cols
            ])
            .list.arg_min() # Returns index of min value
            .replace(idx_to_col) # Map index back to column name
            .alias(new_column_name)
        )

        return df

    def new_column_from_binary_columns_negative_class(
        self,
        df: pl.DataFrame,
        column_name_map: dict,
        new_column_name: str = "",
        dtype: Callable = float,
    ) -> pl.DataFrame:
        return self._new_column_from_binary_columns_negative_class(
            df=df,
            column_name_map=column_name_map,
            new_column_name=new_column_name,
            dtype=dtype,
        )

    #
    # Utilities
    #

    def _resolve_columns_with_dataframe(
        self, df: pl.DataFrame, columns: List[str], default_columns: List[str]
    ) -> List[str]:
        """
        Internal utility function. Uses set logic to ensure
        requested columns are available within the target
        pl.DataFrame.
        """
        available_columns, requested_columns = set(df.columns), set(columns)
        resolved_columns = []

        if len(requested_columns) == 0:
            self.logger.warn(
                f"Unexpected Transform – columns parameter has no values. Defaulting to provided default_columns"
            )
            resolved_columns = default_columns
        elif len(available_columns & requested_columns) == 0:
            self.logger.warn(
                f"Unexpected Transform – none of the requested columns were found in df.columns. Defaulting to provided default_columns"
            )
            resolved_columns = default_columns
        elif len(requested_columns - available_columns) > 0:
            self.logger.warn(
                f"Unexpected Transform – df.columns missing values present in columns parameter: {', '.join([*requested_columns - available_columns])}. Continuing with union."
            )
            resolved_columns = [*(available_columns & requested_columns)]
        else:
            resolved_columns = columns

        return resolved_columns

    def _get_redcap_type_metadata(self, df: pl.DataFrame) -> List[Dict[str, Any]]:
        """
        Extracts REDCap field name, type, and options (the
        metadata) for each column in the target pl.DataFrame
        """

        # REDCap Internal Variable Metadata
        metadata: List[Dict[str, Any]] = [
            {"name": "redcap_data_access_group", "type": "text", "options": {}},
            {"name": "redcap_repeat_instrument", "type": "text", "options": {}},
            {"name": "redcap_repeat_instance", "type": "number", "options": {}},
        ]

        field_types = set(field["field_type"] for field in self.metadata)
        complex_types = {"dropdown", "radio", "checkbox"}
        binary_types = {"yesno"}
        text_types = {"text"}
        skip_types = {"file", "calc", "descriptive", "notes"}

        # Get Column Metadata
        columns = df.columns
        for field in sorted(self.metadata, key=lambda f: f["field_name"]):
            if field["field_name"] in columns:
                field_type = field["field_type"]
                options: dict = {}
                if field_type in complex_types:
                    rgx = self._field_rgx[field_type]
                    # Parse choices string: "1, Yes | 2, No"
                    for option in field["select_choices_or_calculations"].split("|"):
                        if "," not in option: continue
                        k, v = (
                            option.split(",")[0],
                            (",".join(option.split(",")[1:])).strip(),
                        )
                        _k = int(k) if re.match(rgx, k) else str(k)
                        _v = int(v) if re.match(rgx, v) else str(v)
                        options[str(_k)] = _v
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
                            "options": {},
                        }
                    )
                elif field_type in skip_types:
                    metadata.append(
                        {
                            "name": field["field_name"],
                            "type": field["field_type"],
                            "options": {},
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
        self, path: str = "", separator: str = "\t", filetype: str = ".tsv"
    ) -> object:
        for report_key, report_object in self.reports.items():
            filename = f"{report_key}_raw{filetype}"
            filepath = os.path.join(self.cwd, path, filename)
            transformed: pl.DataFrame = report_object["df"]
            transformed.write_csv(
                filepath,
                separator=separator,
                quote_style="non_numeric",
                float_precision=2 # Approx match to %.2f
            )
        return self

    # Export Transformed Reports
    def export_transformed(
        self, path: str = "", separator: str = "\t", filetype: str = ".tsv"
    ) -> object:
        for report_key, report_object in self.reports.items():
            filename = f"{report_key}_transformed{filetype}"
            filepath = os.path.join(self.cwd, path, filename)
            transformed: pl.DataFrame = report_object["transformed"]
            transformed.write_csv(
                filepath,
                separator=separator,
                quote_style="non_numeric",
                float_precision=2
            )
        return self

    # Export Merged Transforms
    def export_merged_transformed(
        self, filepath: str = "transformed-merged_redcap-extract.tsv", separator: str = "\t"
    ) -> object:
        filepath = os.path.join(self.cwd, filepath)
        self.merged.write_csv(
            filepath,
            separator=separator,
            quote_style="non_numeric",
            float_precision=2
        )
        return self

if __name__ == "__main__":
  pass
else:
  pass
