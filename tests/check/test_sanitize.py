"""Test modules in ``sanitize``"""

import pandas as pd
import pytest

from pandas_utils.check.sanitize import (
    check_if_column_exists,
    check_if_columns_exist,
    clean_column_names,
)


class TestSanitize:
    """Test class for ``sanitize``"""

    def test_check_if_column_exists(self, data: pd.DataFrame) -> None:
        """Test ``check_if_column_exists``"""

        with pytest.raises(ValueError):
            check_if_column_exists(column="random_column", data=data)

    def test_check_if_columns_exist(self, data: pd.DataFrame) -> None:
        """Test ``check_if_columns_exist``"""

        with pytest.raises(ValueError):
            check_if_columns_exist(columns=["col_rand1", "col_ran2"], data=data)

    def test_clean_column_names(self, data: pd.DataFrame) -> None:
        """Test ``clean_column_names``"""

        res: pd.DataFrame = clean_column_names(data=data)

        assert res.shape == data.shape
        for column in res.columns:
            for char in column:
                assert isinstance(char, str)
                assert char.isalnum() is True
