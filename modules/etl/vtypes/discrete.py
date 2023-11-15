from .vtype import VType


class SingleDiscrete(VType):
    def __init__(self) -> None:
        super(SingleDiscrete, self).__init__(
            "SingleDiscrete",
            [("filterby", str), ("group", str), ("color", str), ("x", int)],
            int,
        )


class DoubleDiscrete(VType):
    def __init__(self) -> None:
        super(DoubleDiscrete, self).__init__(
            "Discrete",
            [
                ("filterby", str),
                ("group", str),
                ("color", str),
                ("x", int),
                ("y", int),
            ],
            int,
        )
