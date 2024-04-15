from typing import Any, Callable, Union, List, Dict, Tuple
from datetime import datetime
import pandas as pd


class SimpleVType(object):
    def __init__(
        self,
        name: str,
        props: List[Tuple[str, Callable]],
        missing_value: Callable,
    ) -> None:
        self.name = name
        self.props = props
        self.missing_value = missing_value
        # References
        self.validation_errors: List[str] = []

    def __str__(self):
        return f"{self.__dict__}"

    def isvalid(self, df: pd.DataFrame, accessors: Dict[str, Dict[str, str]]) -> bool:
        columns = df.columns
        for pname, ptype in self.props:
            if pname in accessors.keys():
                column = accessors[pname]["field"]
                if column not in columns:
                    self.validation_errors.append(
                        f"VType {self.name.title()} pd.DataFrame argument (df) is missing column defined in accessors argument, {column}"
                    )
                    return False
                else:
                    continue
            else:
                self.validation_errors.append(
                    f"VType {self.name.title()} accessors argument is missing required property, {pname}"
                )
                return False
        return True


class ComplexVType(object):
    def __init__(
        self,
        name: str,
        props: List[Any],
        missing_value: Callable,
    ) -> None:
        self.name = name
        self.props = props
        self.missing_value = missing_value
        # References
        self.validation_errors: List[str] = []

    def __str__(self):
        return f"{self.__dict__}"

    # def isvalid(
    #     self, df: pd.DataFrame, accessorsList: List[Dict[str, Dict[str, str]]]
    # ) -> bool:
    #     """
    #     Extends the VType.isvalid method to operate on a list
    #     of pd.DataFrames and accessors.
    #     """
    #     valid = True
    #     for accessors in accessorsList:
    #         if not super(Compound, self).isvalid(df, accessors):
    #             self.validation_errors.append(
    #                 f"VType {self.name.title()} has invalid accessors. See additional details above."
    #             )
    #             valid = False
    #         else:
    #             continue
    #     return valid

    def isvalid(
        self, df: pd.DataFrame, accessorsList: List[Dict[str, Dict[str, str]]]
    ) -> bool:
        valid = True
        columns = df.columns
        for accessors in accessorsList:
            for pname, ptype in self.props:
                if pname in accessors.keys():
                    column = accessors[pname]["field"]
                    if column not in columns:
                        self.validation_errors.append(
                            f"VType {self.name.title()} pd.DataFrame argument (df) is missing column defined in accessors argument, {column}"
                        )
                        valid = False
                    else:
                        continue
                else:
                    self.validation_errors.append(
                        f"VType {self.name.title()} accessors argument is missing required property, {pname}"
                    )
                    valid = False
        return valid


if __name__ == "__main__":
    pass
else:
    pass
