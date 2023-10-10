from .vtype import VType

class SingleContinuous (VType):
  def __init__ (self: object) -> None:
    super().__init__(
      "SingleContinuous", [
        ("filterby", str),
        ("group", str),
        ("color", str),
        ("x", float)
      ],
      float
    )

class DoubleContinuous (VType):
  def __init__ (self: object) -> None:
    super().__init__(
      "DoubleContinuous", [
        ("filterby", str),
        ("group", str),
        ("color", str),
        ("x", float),
        ("y", float),
      ],
      float
    )

if __name__ == "__main__":
    pass
else:
    pass
