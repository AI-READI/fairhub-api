from .vtype import ComplexVType
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


class Compound(ComplexVType):
    def __init__(self) -> None:
        super(Compound, self).__init__(
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
                Compound,
            ],
            str,
        )


if __name__ == "__main__":
    pass
else:
    pass
