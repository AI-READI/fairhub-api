from .vtype import SimpleVType


class SingleDiscrete(SimpleVType):
    def __init__(self) -> None:
        super(SingleDiscrete, self).__init__(
            "SingleDiscrete",
            [("filterby", str), ("group", str), ("color", str), ("x", int)],
            int,
        )


class DoubleDiscrete(SimpleVType):
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


if __name__ == "__main__":
    pass
else:
    pass
