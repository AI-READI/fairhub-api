from .vtype import VType

class SingleCategorical (VType):
  def __init__ (self: object) -> None:
    super().__init__(
      "SingleCategorical", [
        ("filterby", str),
        ("group", str),
        ("color", str),
        ("value", int),
      ],
      str
    )

class DoubleCategorical (VType):
  def __init__ (self: object) -> None:
    super().__init__(
      "DoubleCategorical", [
        ("filterby", str),
        ("group", str),
        ("subgroup", str),
        ("color", str),
        ("value", int),
      ],
      str
    )

if __name__ == "__main__":
    pass
else:
    pass
