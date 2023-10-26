from .vtype import VType
from .categorical import SingleCategorical, DoubleCategorical
from .discrete import SingleDiscrete, DoubleDiscrete
from .continuous import SingleContinuous, DoubleContinuous
from .timeseries import (
    SingleTimeseries,
    DoubleDiscreteTimeseries,
    DoubleContinuousTimeseries,
)
from typing import Tuple, List, Dict, Callable, Any
import pandas as pd


class Compound(VType):
    def __init__(self: object) -> None:
        raise NotImplementedError
        super().__init__(
            "Compound",
            [
                SingleCategorical,
                DoubleCategorical,
                SingleDiscrete,
                DoubleDiscrete,
                SingleContinuous,
                DoubleContinuous,
                SingleTimeseries,
                DoubleDiscreteTimeseries,
                DoubleContinuousTimeseries,
            ],
            str,
        )

    def isvalid(
        self: object, dfs: pd.DataFrame, accessorsList: List[Dict[str, Dict[str, str]]]
    ) -> bool:
        """
        Extends the VType.isvalid method to operate on a list
        of pd.DataFrames and accessors.
        """
        valid = True
        for accessors in accessorsList:
            if not super(Compound, self).isvalid(df, accessors):
                self.validation_errors.append(
                    f"VType {self.name.title()} has invalid accessors. See additional details above."
                )
                valid = False
            else:
                continue

        return valid
