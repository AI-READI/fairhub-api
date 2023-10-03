from .vtype import VType
from datetime import datetime
import pandas as pd


class Timeseries(VType):
    def __init__(self: object) -> None:
        super().__init__(
            "timeseries",
            [
                ("filterby", str),
                ("subgroup", str),
                ("color", str),
                ("x", datetime),
                ("y", float),
            ],
            pd._libs.tslibs.nattype.NaTType,
        )


if __name__ == "__main__":
    pass
else:
    pass
