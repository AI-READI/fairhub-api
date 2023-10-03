# Library Modules
from typing import Any, Callable, Union, List, Dict, Tuple
from datetime import datetime
import logging, re
from vtypes import VType, Categorical, Continuous, Timeseries, Mixed

# Third-Party Modules
import pandas as pd


class ModuleTransform(object):
    def __init__(self: object, config: Dict[str, Any]) -> None:
        # Logging Config
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
        self.logger = logging.getLogger("VizModETL")
        self.logger.info(f"Initializing")

        #
        # Visualization Variables
        #

        self.vtype = config["vtype"]() if "vtype" in config else None

        self.accessors = config["accessors"] if "accessors" in config else None

        self.transform = config["transform"] if "transform" in config else None

    def _setType(self, key, value):
        for pname, ptype in self.vtype.props:
            if pname == key:
                if value != self.accessors[key]["missingvalue"]:
                    value = ptype(value)
        return value

    def basicTransform(self: object, df: pd.DataFrame) -> object:
        """ """
        self.transformed = []

        if self.vtype.isvalid(df, self.accessors):
            df = df[
                list(set(accessor["field"] for key, accessor in self.accessors.items()))
            ]
            groups, value, func = (
                self.transform["groups"],
                self.transform["value"],
                self.transform["func"],
            )
            transformed = df.groupby(groups)[value][func]()
            # print(transformed)
            for record in transformed.to_dict("records"):
                record = {
                    key: record[accessor["field"]]
                    for key, accessor in self.accessors.items()
                }
                record = {key: self._setType(key, val) for key, val in record.items()}
                self.transformed.append(record)

        else:
            for error in self.vtype.validation_errors:
                self.logger.warning(f"{error}")

        return self


if __name__ == "__main__":
    pass
else:
    pass
