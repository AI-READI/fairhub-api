# Library Modules
from typing import Any, Callable, Union, List, Dict, Tuple
from datetime import datetime
import logging, re, copy
import modules.etl.vtypes as vtypes

# Third-Party Modules
import pandas as pd


class ModuleTransform(object):
    def __init__(
        self,
        config: Dict[str, Any],
        logging_config: Dict[str, str] = {},
    ) -> None:
        #
        # Logging
        #

        # Logging Config Checks
        self.logging_config = (
            config["logging_config"]
            if "logging_config" in config
            else {
                "encoding": "utf-8",
                "filename": "REDCapETL.log",
                "level": logging.DEBUG,
            }
        )

        # Configure Logging
        logging.basicConfig(**self.logging_config)
        self.logger = logging.getLogger("VizModTransform")

        #
        # References
        #

        self.valid: bool = True
        self.transformed: Any

        #
        # Visualization Variables
        #

        # Flag Indicating Whether to Use Strict Typing on Vtype Mapping
        self.strict = config["strict"] if "strict" in config else True

        self.key = config["key"] if "key" in config else None

        self.transforms: List[Dict[str, Any]] = copy.deepcopy(config["transforms"])

        if type(self.transforms) != list:
            self.valid = False
            raise ValueError(
                f"ModuleTransform argument transforms in config must be a list or dict type"
            )
        elif len(self.transforms) < 1:
            self.valid = False
            raise ValueError(
                f"ModuleTransform instantiation missing transforms in config argument"
            )
        else:
            # Transform attribute is there and has one of the correct types (list, dict)
            pass

        # Normalize Transforms to List Type, Check Validity, and Warn on Missing Attributes
        for indexed_transform in enumerate(self.transforms):
            self.valid = True if self._transformIsValid(indexed_transform) else False
        if self.strict and not self.valid:
            raise ValueError(
                f"{self.key}:Missing properties in transforms argument, see log at {self.logging_config['filename']} for details"
            )

        self.logger.info(f"{self.key}:Initialized")

        return

    def _transformIsValid(self, indexed_transform: Tuple[int, Dict[str, Any]]) -> bool:
        """
        Transform validator
        """
        index, transform = indexed_transform
        valid = True
        if "name" not in transform:
            self.logger.error(
                f"{self.key}:Transform at index {index} in transforms list missing name property"
            )
            valid = False
        if "vtype" not in transform:
            self.logger.error(
                f"{self.key}:Transform at index {index} in transforms list missing vtype property"
            )
            valid = False
        if "methods" not in transform:
            self.logger.error(
                f"{self.key}:Transform at index {index} in transforms list missing methods property"
            )
            valid = False
        if "accessors" not in transform:
            self.logger.error(
                f"{self.key}:Transform at index {index} in transforms list missing accessors property"
            )
            valid = False
        return valid

    def _setValueType(
        self,
        vtype: Any,
        name: str,
        record: Dict[str, Any],
        key: str,
        accessors: Dict[str, Dict[str, Any]],
    ) -> Any:
        """
        Element-wise type setting method. If value of
        element is not the missing value, we cast the
        value as the type defined for property in the
        vtype.
        """
        accessor = accessors[key]
        for pname, _ptype in vtype.props:
            if pname == key:
                # Accessor Typing
                ptype = _ptype if "astype" not in accessor else accessor["astype"]
                if ptype != _ptype:
                    self.logger.warning(
                        f"Accessor `{pname}` with type `{ptype}` conflicts with VType definition requiring {_ptype}"
                    )
                    if self.strict:
                        raise ValueError(
                            f"Accessor `{pname}` with type `{ptype}` conflicts with VType definition requiring {_ptype}"
                        )
                # Accessor Name
                pvalue: Any = record[accessor["field"]]
                if "remap" in accessor and accessor["remap"] is not None:
                    pvalue = accessor["remap"](
                        {
                            "name": name,
                            "record": record,
                            "value": pvalue,
                            "key": key,
                            "accessors": accessors,
                        }
                    )
                if pvalue != accessor["missing_value"]:
                    try:
                        pvalue = ptype(pvalue)
                    except (RuntimeError, TypeError) as error:
                        if self.strict:
                            self.logger.warning(
                                f"Unable to cast value {record[key]} to {ptype}"
                            )
                            raise error
                        else:
                            self.logger.warning(
                                f"Unable to cast value {record[key]} to {ptype}"
                            )
                            continue

        return pvalue

    def simpleTransform(self, df: pd.DataFrame) -> object:
        """
        Performs a pd.DataFrame.groupby transform. The
        df is first subset to the relevant fields. A
        groupby function is then applied to the subset
        to create a multi-index (hierarchy) by the
        groups. An aggregate function is then applied
        to the non-grouped column (e.g. count, sum).

        One transform for one VType.
        """
        self.transformed = []
        transform: Dict[str, Any] = (
            self.transforms.pop()
        )  # simple transforms have only one transform object
        name, vtype, methods, accessors = (
            transform["name"],
            getattr(vtypes, transform["vtype"])(),
            transform["methods"],
            transform["accessors"],
        )
        if vtype.isvalid(df, accessors):
            temp = df[
                list(set(accessor["field"] for key, accessor in accessors.items()))
            ]
            for method in methods:
                groups, value, func = method["groups"], method["value"], method["func"]
                grouped = temp.groupby(groups, as_index=False)
                temp = getattr(grouped, func)()
            transformed = temp

            for record in transformed.to_dict("records"):
                record = {
                    key: self._setValueType(vtype, name, record, key, accessors)
                    for key, accessor in accessors.items()
                }
                record = {"name": name} | record
                self.transformed.append(record)

        else:
            for error in vtype.validation_errors:
                self.logger.warning(f"{error}")

        if len(vtype.validation_errors) == 0:
            self.logger.info(f"{self.key}:Complete - simpleTransform")

        return self

    def compoundTransform(self, df: pd.DataFrame) -> object:
        """
        For each transform, performs a pd.DataFrame.groupby
        transform. The df is first subset to the relevant
        fields. A groupby function is then applied to the
        subset to create a multi-index (hierarchy) by the
        groups. An aggregate function is then applied to the
        non-grouped column (e.g. count, sum).

        All transforms are combined into a single flat
        transform. Transforms must be identical VType,
        e.g. [transformA, transformB, ...]
        """
        self.transformed = []

        for transform in self.transforms:
            name, vtype, methods, accessors = (
                transform["name"],
                getattr(vtypes, transform["vtype"])(),
                transform["methods"],
                transform["accessors"],
            )
            if vtype.isvalid(df, accessors):
                temp = df[
                    list(set(accessor["field"] for key, accessor in accessors.items()))
                ]
                for method in methods:
                    groups, value, func = (
                        method["groups"],
                        method["value"],
                        method["func"],
                    )
                    grouped = temp.groupby(groups, as_index=False)
                    temp = getattr(grouped, func)()
                transformed = temp

                for record in transformed.to_dict("records"):
                    record = {
                        key: self._setValueType(vtype, name, record, key, accessors)
                        for key, accessor in accessors.items()
                    }
                    record = {"name": name} | record
                    self.transformed.append(record)

            else:
                for error in vtype.validation_errors:
                    self.logger.warning(f"{error}")

        if len(vtype.validation_errors) == 0:
            self.logger.info(f"{self.key}:Complete - compoundTransform")

        return self

    def mixedTransform(self, df: pd.DataFrame) -> object:
        """
        For each transform, performs a pd.DataFrame.groupby
        transform. The df is first subset to the relevant
        fields. A groupby function is then applied to the
        subset to create a multi-index (hierarchy) by the
        groups. An aggregate function is then applied to the
        non-grouped column (e.g. count, sum).

        Transforms are kept distinct inserted into a dictionary,
        e.g. {nameA: transformA, nameB: transformB, ...}.
        Transforms can be heterogenous VTypes.
        """
        self.transformed = {}
        for transform in self.transforms:
            name, vtype, methods, accessors = (
                transform["name"],
                getattr(vtypes, transform["vtype"])(),
                transform["methods"],
                transform["accessors"],
            )
            if vtype.isvalid(df, accessors):
                temp = df[
                    list(set(accessor["field"] for key, accessor in accessors.items()))
                ]
                for method in methods:
                    groups, value, func = (
                        method["groups"],
                        method["value"],
                        method["func"],
                    )
                    grouped = temp.groupby(groups, as_index=False)
                    temp = getattr(grouped, func)()
                transformed = temp

                subtransform = []
                for record in transformed.to_dict("records"):
                    record = {
                        key: self._setValueType(vtype, name, record, key, accessors)
                        for key, accessor in accessors.items()
                    }
                    record = {"name": name} | record
                    subtransform.append(record)
                self.transformed[name] = subtransform

            else:
                for error in vtype.validation_errors:
                    self.logger.warning(f"{error}")

        if len(vtype.validation_errors) == 0:
            self.logger.info(f"{self.key}:Complete - mixedTransform")

        return self


if __name__ == "__main__":
    pass
else:
    pass
