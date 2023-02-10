"""Check sanity of dataframes"""

import re

import pandas as pd


def check_if_column_exists(column: str, data: pd.DataFrame):
    """Check the column exists in the dataframe.
    Usually used to cross-check against a dataframe.

    :param column: Name of the column
    :type column: ``str``
    :param data: Dataframe object to check against.
    :type data: ``pd.DataFrame``
    :raises ValueError: If the column is not found in the dataframe.
    :example:
        >>> from pandas_utils.check.sanitize import check_if_column_exists
        >>> check_if_column_exists(column="random_column", data=data)
    """

    columns = data.columns
    if column not in columns:
        raise ValueError(f"{column} not found in {columns}")


def check_if_columns_exist(columns: list, data: pd.DataFrame):
    """Check the column exists in the dataframe.
    Usually used to cross-check against a dataframe.

    :param columns: List of columns
    :type columns: ``list``
    :param data: Dataframe object to check against.
    :type data: ``pd.DataFrame``
    :raises ValueError: If any of the columns is not found in the dataframe.
    :example:
        >>> from pandas_utils.check.sanitize import check_if_columns_exist
        >>> check_if_columns_exist(columns=["col_rand1", "col_ran2"], data=data)
    """

    for column in columns:
        if column not in data.columns:
            raise ValueError(f"{column} not found in {data.columns}")


def clean_column(column: str, is_lower: bool = True, default_char: str = "") -> str:
    """Clean a column name.

    :param column: Name of column.
    :type column: ``str``
    :param is_lower: If cleaned column name should be in lowercase, defaults to True
    :type is_lower: ``bool, optional``
    :param default_char: What to replace illegal characters with, defaults to "".
        Another great choice is "_"., defaults to ""
    :type default_char: ``str, optional``
    :return: Dataframe with clean column names.
    :rtype: ``str``
    :example:
        >>> from pandas_utils.check.sanitize import clean_column
        >>> column_new = clean_column(
        >>>     column=column,
        >>>     is_lower=is_lower,
        >>>     default_char=default_char,
        >>> )
    """

    if is_lower:
        column = column.lower()

    pattern = "[^a-zA-Z0-9]"

    return re.sub(pattern=pattern, repl=default_char, string=column)


def clean_column_names(
    data: pd.DataFrame,
    is_lower: bool = True,
    default_char: str = "",
) -> pd.DataFrame:
    """Clean columns of a dataframe.

    :param data: Dataframe object.
    :type data: ``pd.DataFrame``
    :param is_lower: If cleaned column name should be in lowercase, defaults to True
    :type is_lower: ``bool, optional``
    :param default_char: What to replace illegal characters with, defaults to "".
        Another great choice is "_".
    :type default_char: ``str, optional``
    :return: Dataframe with clean column names.
    :rtype: ``pd.DataFrame``
    :example:
        >>> from pandas_utils.check.sanitize import clean_column_names
        >>> res: pd.DataFrame = clean_column_names(data=data)
    """

    data.columns = [
        clean_column(
            column=column,
            is_lower=is_lower,
            default_char=default_char,
        )
        for column in data.columns
    ]

    return data
