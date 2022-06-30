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


def join_two_dfs(df_1: pd.DataFrame, df_2: pd.DataFrame) -> pd.DataFrame:
    """
    Joins two DataFrames, re-sets axis as a column and returns the processed DataFrame
    :param df_1: first DataFrame
    :type df_1: pd.DataFrame
    :param df_2: second DataFrame
    :type df_2: pd.DataFrame
    :return: joined DataFrames
    :rtype: pd.DataFrames
    """
    df_3 = df_1.join(df_2, how="outer").dropna()
    df_3.reset_index(level=0, inplace=True)
    df_3.rename(columns={"index": "dates"}, inplace=True)

    return df_3
