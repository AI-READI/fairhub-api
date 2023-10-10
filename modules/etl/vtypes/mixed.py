from typing import Any, Callable, Union, List, Dict, Tuple
from .vtype import VType
from .categorical import SingleCategorical, DoubleCategorical
from .discrete import SingleDiscrete, DoubleDiscrete
from .continuous import SingleContinuous, DoubleContinuous
from .timeseries import SingleTimeseries, DoubleDiscreteTimeseries, DoubleContinuousTimeseries
from .compound import Compound
import pandas as pd

class Mixed (VType):
  def __init__ (self: object) -> None:
    raise NotImplementedError
    super().__init__(
      "Mixed", [
        SingleCategorical,
        DoubleCategorical,
        SingleDiscrete,
        DoubleDiscrete,
        SingleContinuous,
        DoubleContinuous,
        SingleTimeseries,
        DoubleDiscreteTimeseries,
        DoubleContinuousTimeseries,
        Compound
      ], str
    )

  def isvalid (self: object, dfs: pd.DataFrame, accessorsList: List[Dict[str, Dict[str, str]]]) -> bool:
    """
    Extends the VType.isvalid method to operate on a list
    of pd.DataFrames and accessors.
    """
    valid = True
    for accessors in accessorsList:
      if not super(Compound, self).isvalid(df, accessors):
        self.validation_errors.append(f"VType {self.name.title()} has invalid accessors. See additional details above.")
        valid = False
      else:
        continue

if __name__ == "__main__":
    pass
else:
    pass
