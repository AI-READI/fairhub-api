# Library Modules
from typing import Any, Callable, Union, List, Dict, Tuple
from datetime import datetime
import logging, re
from vtypes import *

# Third-Party Modules
import pandas as pd

class ModuleTransform (object):

  def __init__(self: object, config: Dict[str, Dict[str, Any]], logging_config: Dict[str, str] = {}) -> None:

    #
    # Logging
    #

    # Logging Config Checks
    self.logging_config = {}
    self.logging_config["encoding"] = logging_config["encoding"] \
      if "encoding" in logging_config \
      else "utf-8"
    self.logging_config["filename"] = logging_config["filename"] \
      if "filename" in logging_config \
      else "REDCapETL.log"
    self.logging_config["level"] = getattr(logging, logging_config["level"].upper) \
      if "level" in logging_config \
      else logging.DEBUG

    # Configure Logging
    logging.basicConfig(**self.logging_config)
    self.logger = logging.getLogger("VizModETL")
    self.logger.info(f"Initializing")

    #
    # References
    #

    self.valid_transforms = True

    #
    # Visualization Variables
    #

    # Flag Indicating Whether to Use Strict Typing on Vtype Mapping
    self.strict = config["strict"] \
      if "strict" in config \
      else True

    self.vtype = config["vtype"]() \
      if "vtype" in config \
      else None

    self.key = config["key"] \
      if "key" in config \
      else None

    self.transforms = config["transforms"] \
      if "transforms" in config \
      else None

    if self.transforms is None:
      self.valid_transforms = False
      raise ValueError(f"ModuleTransform instantiation missing transforms argument")

    # Normalize Transforms List Type, Check Validity, and Warn on Missing Attributes
    self.transformList = self.transforms if (type(self.transforms) == list) else [self.transforms]
    for i, transform in enumerate(self.transformList):
      if "name" not in transform:
        self.logger.error(f"Transform at index {i} in transforms list missing name property")
        self.valid_transforms = False
      if "method" not in transform:
        self.logger.error(f"Transform at index {i} in transforms list missing method property")
        self.valid_transforms = False
      if "accessors" not in transform:
        self.logger.error(f"Transform at index {i} in transforms list missing accessors property")
        self.valid_transforms = False
    if (self.strict and not self.valid_transforms):
      raise ValueError(f"Missing properties in transforms argument, see log at {self.logging_config['filename']} for details")

    return

  def _setValueType (self, record, key, accessor):
    """
    Element-wise type setting method. If value of
    element is not the missing value, we cast the
    value as the type defined for property in the
    vtype.
    """
    for pname, _ptype in self.vtype.props:
      if pname == key:
        # Accessor Typing
        ptype = _ptype \
          if "astype" not in accessor \
          else accessor["astype"]
        if ptype != _ptype:
          self.logger.warning(f"Accessor `{pname}` with type `{ptype}` conflicts with VType definition requiring {_ptype}")
          if self.strict:
            raise ValueError(f"Accessor `{pname}` with type `{ptype}` conflicts with VType definition requiring {_ptype}")
        # Accessor Name
        pvalue = record[accessor["field"]]
        if pvalue != accessor["missing_value"]:
          try:
            pvalue = ptype(pvalue)
          except (RuntimeError, TypeError) as error:
            if self.strict:
              self.logger.warning(f"Unable to cast value {record[key]} to {ptype}")
              raise error
            else:
              self.logger.warning(f"Unable to cast value {record[key]} to {ptype}")
              continue

    return pvalue

  def simpleTransform (self: object, df: pd.DataFrame) -> object:
    """
    Performs a pd.DataFrame.groupby transform. The
    df is first subset to the relevant fields. A
    groupby function is then applied to the subset
    to create a multi-index (hierarchy) by the
    groups. An aggregate function is then applied
    to the non-grouped column (e.g. count, sum).
    """
    transform = self.transformList.pop()
    name, method, accessors = transform["name"], transform["method"], transform["accessors"]
    self.transformed = []

    if self.vtype.isvalid(df, accessors):
      temp = df[list(set(accessor["field"] for key, accessor in accessors.items()))]
      groups, value, func = method["groups"], method["value"], method["func"]
      grouped = temp.groupby(groups, as_index = False)
      transformed = getattr(grouped, func)()

      for record in transformed.to_dict("records"):
        record = {key: self._setValueType(record, key, accessor) for key, accessor in accessors.items()}
        record = {"name": name} | record
        self.transformed.append(record)

    else:

      for error in self.vtype.validation_errors:
        self.logger.warning(f"{error}")

    return self

  def compoundTransform (self: object, df: pd.DataFrame) -> object:
    """
    For each transform, performs a pd.DataFrame.groupby
    transform. The df is first subset to the relevant
    fields. A groupby function is then applied to the
    subset to create a multi-index (hierarchy) by the
    groups. An aggregate function is then applied to the
    non-grouped column (e.g. count, sum).

    All transforms are combined into a single flat
    transform.
    """
    self.transformed = []

    for transform in self.transformList:

      name, method, accessors = transform["name"], transform["method"], transform["accessors"]
      if self.vtype.isvalid(df, accessors):
        temp = df[list(set(accessor["field"] for key, accessor in accessors.items()))]
        groups, value, func = method["groups"], method["value"], method["func"]
        grouped = temp.groupby(groups, as_index = False)
        transformed = getattr(grouped, func)()

        for record in transformed.to_dict("records"):
          record = {key: self._setValueType(record, key, accessor) for key, accessor in accessors.items()}
          record = {"name": name} | record
          self.transformed.append(record)

      else:

        for error in self.vtype.validation_errors:
          self.logger.warning(f"{error}")

    return self

  def mixedTransform (self: object, df: pd.DataFrame) -> object:
    """
    For each transform, performs a pd.DataFrame.groupby
    transform. The df is first subset to the relevant
    fields. A groupby function is then applied to the
    subset to create a multi-index (hierarchy) by the
    groups. An aggregate function is then applied to the
    non-grouped column (e.g. count, sum).

    Transforms are kept distinct and appended to a list,
    e.g. [t_1, t_2, ..., t_n]
    """
    self.transformed = {}

    for transform in self.transformList:

      name, method, accessors = transform["name"], transform["method"], transform["accessors"]
      if self.vtype.isvalid(df, accessors):
        temp = df[list(set(accessor["field"] for key, accessor in accessors.items()))]
        groups, value, func = method["groups"], method["value"], method["func"]
        grouped = temp.groupby(groups, as_index = False)
        transformed = getattr(grouped, func)()

        subtransform = []
        for record in transformed.to_dict("records"):
          record = {key: self._setValueType(record, key, accessor) for key, accessor in accessors.items()}
          record = {"name": name} | record
          subtransform.append(record)
        self.transformed[name] = subtransform

      else:

        for error in self.vtype.validation_errors:
          self.logger.warning(f"{error}")

    return self


if __name__ == "__main__":
  pass
else:
  pass

