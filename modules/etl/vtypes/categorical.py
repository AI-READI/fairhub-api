from .vtype import SimpleVType


class SingleCategorical(SimpleVType):
    def __init__(self) -> None:
        super(SingleCategorical, self).__init__(
            "SingleCategorical",
            [
                ("filterby", str),
                ("group", str),
                ("color", str),
                ("value", int),
            ],
            str,
        )


class DoubleCategorical(SimpleVType):
    def __init__(self) -> None:
        super(DoubleCategorical, self).__init__(
            "DoubleCategorical",
            [
                ("filterby", str),
                ("group", str),
                ("subgroup", str),
                ("color", str),
                ("value", int),
            ],
            str,
        )


if __name__ == "__main__":
    pass
else:
    pass
