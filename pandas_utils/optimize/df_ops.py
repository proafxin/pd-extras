"""Optimize dataframe operations"""

import re

import numpy as np
import pandas as pd


def select_columns_from_dataframe(
    data: pd.DataFrame,
    columns: list,
) -> pd.DataFrame:
    """Get a dataframe consisting columns from a dataframe
    This is the fastest approach from some tests conducted.
    ```df.iloc[indices, column_indices]``` is a close second.

    :param data: Dataframe to take columns from.
    :type data: ```pd.DataFrame```
    :param columns: List of columns.
    :type columns: ```list```
    :return: Dataframe with the selected columns.
    :rtype: ```pd.DataFrame```
    """

    check_if_columns_exist(columns=columns, data=data)

    indices: dict = {column: idx for idx, column in enumerate(data.columns)}

    selected_indices: list = []
    for column in columns:
        selected_indices.append(indices[column])

    return np.take(a=data, indices=selected_indices, axis=1)


def check_if_column_exists(column: str, data: pd.DataFrame):
    """Check the column exists in the dataframe.
    Usually used to cross-check against a dataframe.

    :param column: Name of the column
    :type column: ```str```
    :param data: Dataframe object to check against.
    :type data: ```pd.DataFrame```
    :raises ValueError: If the column is not found in the dataframe.
    """

    columns = data.columns
    if column not in columns:
        raise ValueError(f"{column} not found in {columns}")


def check_if_columns_exist(columns: list, data: pd.DataFrame):
    """Check the column exists in the dataframe.
    Usually used to cross-check against a dataframe.

    :param columns: List of columns
    :type columns: ```list```
    :param data: Dataframe object to check against.
    :type data: ```pd.DataFrame```
    :raises ValueError: If any of the columns is not found in the dataframe.
    """

    for column in columns:
        if column not in data.columns:
            raise ValueError(f"{column} not found in {data.columns}")


def clean_column(column: str, is_lower: bool = True, default_char: str = "") -> str:
    if is_lower:
        column = column.lower()

    pattern = "[^a-zA-Z0-9]"

    return re.sub(pattern=pattern, repl=default_char, string=column)


def clean_column_names(
    data: pd.DataFrame,
    is_lower: bool = True,
    default_char: str = "",
) -> pd.DataFrame:
    data.columns = [
        clean_column(
            column=column,
            is_lower=is_lower,
            default_char=default_char,
        )
        for column in data.columns
    ]

    return data
