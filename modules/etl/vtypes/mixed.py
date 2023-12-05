from typing import Any, Callable, Union, List, Dict, Tuple
from .vtype import ComplexVType
from .categorical import SingleCategorical, DoubleCategorical
from .discrete import SingleDiscrete, DoubleDiscrete
from .continuous import SingleContinuous, DoubleContinuous
from .timeseries import (
    SingleTimeseries,
    DoubleDiscreteTimeseries,
    DoubleContinuousTimeseries,
)
from .compound import Compound
import pandas as pd


class Mixed(ComplexVType):
    def __init__(self) -> None:
        raise NotImplementedError
        super(Mixed, self).__init__(
            "Mixed",
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
                Compound,
            ],
            str,
        )

if __name__ == "__main__":
    pass
else:
    pass
