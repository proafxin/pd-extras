"""Test df_ops"""

import numpy as np
import pandas as pd

from pandas_utils.optimize.df_ops import get_rows, select_columns_from_dataframe


class TestDfOps:
    """Test ``df_ops``"""

    def test_select_columns(self, data: pd.DataFrame) -> None:
        """Test ``select_columns_from_dataframe``"""

        columns = np.random.choice(data.columns, size=3)
        res = select_columns_from_dataframe(data=data, columns=list(columns))

        assert isinstance(res, pd.DataFrame)
        assert res.shape[0] == data.shape[0]
        assert res.shape[1] == 3

        assert np.array_equal(res.to_numpy(), data[columns].to_numpy())

    def test_get_rows(self, data: pd.DataFrame) -> None:
        """Test ``get_rows``"""

        columns = np.random.choice(data.columns, size=3)
        rows = get_rows(data=data, columns=list(columns))

        assert isinstance(rows, np.ndarray)
        assert rows.shape[0] == data.shape[0]
        assert rows.shape[1] == 3

        assert np.array_equal(data[columns].to_numpy(), rows) is True
