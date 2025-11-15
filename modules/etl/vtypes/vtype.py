from typing import Any, Callable, List, Dict, Tuple, Type, Union
import polars as pl

# A property on a SimpleVType: ("value", int), ("filterby", str), etc.
VTypeProp = Tuple[str, Callable[..., Any]]

# A child vtype class included inside ComplexVType
VTypeClass = Type["BaseVType"]

# ComplexVType may accept either real props (VTypeProp)
# or child vtype classes (VTypeClass)
PropsList = List[Union[VTypeProp, VTypeClass]]


class BaseVType:
    def __init__(
        self,
        name: str,
        props: PropsList,
        missing_value: Callable[..., Any],
    ) -> None:
        self.name = name
        self.props = props
        self.missing_value = missing_value
        self.validation_errors: List[str] = []

    def __str__(self) -> str:
        return f"{self.__dict__}"

    def _validate_single_accessor(
        self,
        df_cols: set,
        accessors: Dict[str, Dict[str, str]]
    ) -> bool:
        ok = True
        vname = self.name.title()

        for item in self.props:
            # ComplexVType entries may be classes, skip them
            if not isinstance(item, tuple):
                continue

            pname, _ = item

            field_info = accessors.get(pname)
            if not field_info:
                self.validation_errors.append(
                    f"VType {vname} accessors argument is missing required property, {pname}"
                )
                ok = False
                continue

            column = field_info["field"]
            if column not in df_cols:
                self.validation_errors.append(
                    f"VType {vname} pl.DataFrame argument (df) is missing column "
                    f"defined in accessors argument, {column}"
                )
                ok = False

        return ok


class SimpleVType(BaseVType):
    def isvalid(
        self,
        df: pl.DataFrame,
        accessors: Dict[str, Dict[str, str]]
    ) -> bool:
        return self._validate_single_accessor(set(df.columns), accessors)


class ComplexVType(BaseVType):
    def isvalid(
        self,
        df: pl.DataFrame,
        accessors_list: List[Dict[str, Dict[str, str]]]
    ) -> bool:
        df_cols = set(df.columns)
        valid = True

        for accessors in accessors_list:
            if not self._validate_single_accessor(df_cols, accessors):
                valid = False

        return valid


if __name__ == "__main__":
    pass
else:
    pass
