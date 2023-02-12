"""Flatten dataframes"""

from dataclasses import dataclass, field
from typing import Union

import numpy as np
import pandas as pd


@dataclass
class Flattener:
    """Class to flatten dataframes.

    :example:
        >>> from pandas_utils.extra.flatten import Flattener
        >>> flattener = Flattener(num_rows_to_check=num_rows_to_check, depth=depth)
        >>> # Flatten the dataframe
        >>> flat_data = flattener.flatten(data=data)
        >>> # Check whether a column has nested data or not
        >>> column_info = flattener.get_column_info(data=data)
    """

    num_rows_to_check: int
    depth: int = field(default=1)
    sep: str = field(default=".")

    def get_column_info(self, data: pd.DataFrame) -> list:
        """Check whether a certain column is nested or not.

        :param data: Dataframe to check.
        :type data: ``pd.DataFrame``
        :return: List of booleans.
            True if the corresponding column has nested data.
        :rtype: ``list``
        """

        column_info = []

        if isinstance(data, dict):
            keys = data.keys()
            data = pd.json_normalize(data=data)
            columns = data.columns.tolist()
            for key in keys:
                if key in columns:
                    column_info.append(False)
                else:
                    column_info.append(True)

            return column_info

        rows = data.iloc[: self.num_rows_to_check]
        for column in data.columns:
            values = rows[column].to_numpy()
            num_nested = 0

            for value in values:
                if isinstance(value, dict):
                    num_nested += 1
                elif isinstance(value, list) and len(value) > 0:
                    if isinstance(value[0], dict):
                        num_nested += 1
            if num_nested * 2 >= self.num_rows_to_check:
                column_info.append(True)
            else:
                column_info.append(False)

        return column_info

    def _flatten(
        self, data: Union[pd.DataFrame, dict], depth: int = 0, depth_cur: int = 0
    ) -> pd.DataFrame:
        if isinstance(data, dict):
            data = pd.json_normalize(data=data)
        else:
            data = pd.json_normalize(data=data.to_dict("records"), sep=self.sep)

        if depth <= depth_cur or depth < 1:
            return data

        columns = data.columns
        column_info = self.get_column_info(data=data)

        helper_col: str = "___ID___"
        data[helper_col] = np.arange(data.shape[0]) + 1
        flat_data = data.copy()

        if np.array(column_info).sum() == 0:
            return flat_data.drop(helper_col, axis=1)

        for column, info in zip(columns, column_info):
            if info:
                records = data.to_dict("records")
                flat_data = flat_data.drop(column, axis=1)

                cur_flat_data = pd.json_normalize(
                    data=records,
                    record_path=column,
                    meta=helper_col,
                    record_prefix=column + self.sep,
                )

                flat_data = pd.merge(
                    left=flat_data,
                    right=cur_flat_data,
                    on=helper_col,
                    how="outer",
                )

        flat_data = flat_data.drop(labels=helper_col, axis=1)

        return self._flatten(data=flat_data, depth=depth, depth_cur=depth_cur + 1)

    def flatten(self, data: Union[dict, pd.DataFrame]) -> pd.DataFrame:
        """Return a normalized dataframe.

        :param data: Pandas dataframe to normalize.
        :type data: ``pd.DataFrame``
        :return: Normalized dataframe.
        :rtype: ``pd.DataFrame``
        """

        return self._flatten(data=data, depth=self.depth, depth_cur=0)
