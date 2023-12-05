from .vtype import SimpleVType


class SingleContinuous(SimpleVType):
    def __init__(self) -> None:
        super(SingleContinuous, self).__init__(
            "SingleContinuous",
            [("filterby", str), ("group", str), ("color", str), ("x", float)],
            float,
        )


class DoubleContinuous(SimpleVType):
    def __init__(self) -> None:
        super(DoubleContinuous, self).__init__(
            "DoubleContinuous",
            [
                ("filterby", str),
                ("group", str),
                ("color", str),
                ("x", float),
                ("y", float),
            ],
            float,
        )


if __name__ == "__main__":
    pass
else:
    pass
