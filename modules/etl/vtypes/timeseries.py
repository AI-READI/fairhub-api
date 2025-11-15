from .vtype import SimpleVType
from datetime import datetime


class SingleTimeseries(SimpleVType):
    def __init__(self) -> None:
        super(SingleTimeseries, self).__init__(
            "SingleTimeseries",
            [
                ("filterby", str),
                ("group", str),
                ("x", datetime),
            ],
            str,
        )


class DoubleDiscreteTimeseries(SimpleVType):
    def __init__(self) -> None:
        super(DoubleDiscreteTimeseries, self).__init__(
            "DoubleDiscreteTimeseries",
            [
                ("filterby", str),
                ("group", str),
                ("x", str),
                ("y", int),
            ],
            str,
        )


class DoubleContinuousTimeseries(SimpleVType):
    def __init__(self) -> None:
        super(DoubleContinuousTimeseries, self).__init__(
            "DoubleContinuousTimeseries",
            [
                ("filterby", str),
                ("group", str),
                ("x", str),
                ("y", float),
            ],
            str,
        )


if __name__ == "__main__":
    pass
else:
    pass
