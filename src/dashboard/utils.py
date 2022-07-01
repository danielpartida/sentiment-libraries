from typing import Tuple

import pandas as pd


def get_color_and_symbol(number: float) -> Tuple:
    """
    html_colors = "https://htmlcolorcodes.com/colors/shades-of-green/"
    :return: green or red depending if the last return was positive or negative
    :rtype: Tuple(str, str)
    """
    if number > 0:
        return "#50C878", "fa fa-angle-up"
    else:
        return "#D22B2B", "fa fa-angle-down"
