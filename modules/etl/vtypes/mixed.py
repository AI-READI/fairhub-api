from .vtype import VType
from .categorical import Categorical
from .continuous import Continuous
from .timeseries import Timeseries
from datetime import datetime

class Mixed (VType):
  def __init__ (self: object) -> None:
    raise NotImplementedError
    super().__init__(
      "mixed", [
        Categorical,
        Continuous,
        Timeseries
      ], str
    )

if __name__ == "__main__":
  pass
else:
  pass
