from .vtype import VType


class Continuous(VType):
    def __init__(self: object) -> None:
        super().__init__(
            "continuous",
            [
                ("filterby", str),
                ("subgroup", str),
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
