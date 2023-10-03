from .vtype import VType


class Categorical(VType):
    def __init__(self: object) -> None:
        super().__init__(
            "categorical",
            [
                ("filterby", str),
                ("group", str),
                ("subgroup", str),
                ("color", str),
                ("value", float),
            ],
            str,
        )


if __name__ == "__main__":
    pass
else:
    pass
