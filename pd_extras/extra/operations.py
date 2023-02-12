"""Some extra operations"""

import numpy as np
import pandas as pd


def auto_join(
    left: pd.DataFrame, right: pd.DataFrame, how: str = "inner"
) -> pd.DataFrame:
    """Automatically join two dataframes based on common columns.

    :param left: Left dataframe.
    :type left: ``pd.DataFrame``
    :param right: Right dataframe.
    :type right: ``pd.DataFrame``
    :param how: How to join the dataframes, defaults to "inner".
    :type how: ``str, optional``
    :raises ValueError: If no common column is found.
    :return: Dataframe with the join output.
    :rtype: ``pd.DataFrame``
    :example:
        >>> from pandas_utils.extra.operations import auto_join
        >>> joined_df = auto_join(left=left, right=right)
    """

    common_cols = list(set(left.columns).intersection(set(right.columns)))
    if len(common_cols) < 1:
        raise ValueError("No common columns found")

    joined_df: pd.DataFrame = pd.merge(
        left=left,
        right=right,
        on=common_cols,
        how=how,
    )

    return joined_df


def generate_random_dataframe(
    num_int_cols: int,
    num_float_cols: int,
    size: int,
    low_int: int = 1,
    high_int: int = 100,
    low_float: float = 0,
    high_float: float = 10,
) -> pd.DataFrame:
    """Generate a dataframe with random data.

    :param num_int_cols: Number of integer columns.
    :type num_int_cols: ``int``
    :param num_float_cols: Number of float columns.
    :type num_float_cols: ``int``
    :param size: Number of rows.
    :type size: ``int``
    :param low_int: Lower bound for int columns, defaults to 1.
    :type low_int: ``int, optional``
    :param high_int: Upper bound for int columns, defaults to 100.
    :type high_int: ``int, optional``
    :param low_float: Lower bound for float columns, defaults to 0.
    :type low_float: ``float, optional``
    :param high_float: Upper bound for float columns, defaults to 10.
    :type high_float: ``float, optional``
    :return: Dataframe with ``num_int_cols`` int columns and ``num_float_cols`` float columns.
    :rtype: ``pd.DataFrame``
    :example:
        >>> from pandas_utils.extra.operations import generate_random_dataframe
        >>> size = 100_000
        >>> data = generate_random_dataframe(num_int_cols=2, num_float_cols=3, size=size)
    """

    data = pd.DataFrame()
    for idx in np.arange(num_int_cols) + 1:
        column = f"int{idx}"
        data[column] = np.random.randint(low=low_int, high=high_int, size=size)
    for idx in np.arange(num_float_cols) + data.shape[1] + 1:
        column = f"float{idx}"
        data[column] = np.random.uniform(low=low_float, high=high_float, size=size)

    return data
