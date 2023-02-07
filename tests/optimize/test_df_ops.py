"""Test df_ops"""

import numpy as np
import pandas as pd
import pytest

from pandas_utils.optimize.df_ops import (
    check_if_column_exists,
    check_if_columns_exist,
    select_columns_from_dataframe,
)


class TestDfOps:
    """Test ```df_ops```"""

    def test_select_columns(self, data: pd.DataFrame) -> None:
        """Test ```select_columns_from_dataframe```"""

        columns = np.random.choice(data.columns, size=3)
        res = select_columns_from_dataframe(data=data, columns=list(columns))

        assert isinstance(res, pd.DataFrame)
        assert res.shape[0] == data.shape[0]
        assert res.shape[1] == 3

    def test_check_if_column_exists(self, data: pd.DataFrame) -> None:
        """Test ```check_if_column_exists```"""

        with pytest.raises(ValueError):
            check_if_column_exists(column="random_column", data=data)

    def test_check_if_columns_exist(self, data: pd.DataFrame) -> None:
        """Test ```check_if_columns_exist```"""

        with pytest.raises(ValueError):
            check_if_columns_exist(columns=["col_rand1", "col_ran2"], data=data)
