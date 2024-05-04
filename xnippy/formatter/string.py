from __future__ import annotations
import os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Union
    from typing import List, KeysView


class String:
    @staticmethod
    def calc_num_char(input_var: Union[str, int]):
        return len(str(input_var))
        
    @staticmethod
    def calc_max_char(input_list: Union[List, KeysView]):
        return max([String.calc_num_char(i) for i in input_list])

    @staticmethod
    def line_of_char(char: str, num_char: int):
        return char * num_char

