"""Optimize dataframe operations"""

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
