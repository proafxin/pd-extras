"""Optimize dataframe operations"""


import numpy as np
import pandas as pd

from pandas_utils.check.sanitize import check_if_columns_exist


def select_columns_from_dataframe(
    data: pd.DataFrame,
    columns: list,
) -> pd.DataFrame:
    """Get a dataframe consisting columns from a dataframe
    This is the fastest approach from some tests conducted.
    ``df.iloc[indices, column_indices]`` is a close second.

    :param data: Dataframe to take columns from.
    :type data: ``pd.DataFrame``
    :param columns: List of columns.
    :type columns: ``list``
    :return: Dataframe with the selected columns.
    :rtype: ``pd.DataFrame``
    """

    check_if_columns_exist(columns=columns, data=data)

    indices: dict = {column: idx for idx, column in enumerate(data.columns)}

    selected_indices: list = []
    for column in columns:
        selected_indices.append(indices[column])

    return np.take(a=data, indices=selected_indices, axis=1)


def get_rows(data: pd.DataFrame, columns: list) -> np.ndarray:
    """Get iterable rows for the selected columns.

    :param data: Pandas dataframe to select columns from.
    :type data: ``pd.DataFrame``
    :param columns: List of columns.
    :type columns: ``list``
    :return: Numpy array containing iterable rows.
    :rtype: ``np.ndarray``
    """

    check_if_columns_exist(columns=columns, data=data)

    data = select_columns_from_dataframe(data=data, columns=columns)
    rows = data.to_numpy()

    return rows
