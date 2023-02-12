"""Test operations module"""

import numpy as np
import pandas as pd
import pytest
from pd_extras.check.sanitize import check_if_columns_exist
from pd_extras.extra.operations import auto_join, generate_random_dataframe


def test_generate_random_dataframe():
    """Test ``generate_random_dataframe``"""

    size = 100_000
    data = generate_random_dataframe(num_int_cols=2, num_float_cols=3, size=size)

    assert isinstance(data, pd.DataFrame)
    assert data.shape[0] == size
    assert data.shape[1] == 2 + 3

    dtypes = data.dtypes
    _, counts = np.unique(dtypes, return_counts=True)
    assert len(counts) == 2
    assert set(counts) == set([2, 3])


def test_auto_join(data: pd.DataFrame):
    """Test ``auto_join``"""

    left = generate_random_dataframe(num_int_cols=2, num_float_cols=1, size=100)
    right = generate_random_dataframe(num_int_cols=1, num_float_cols=2, size=1000)

    joined_df = auto_join(left=left, right=right)

    assert isinstance(joined_df, pd.DataFrame)
    assert joined_df.shape[1] == 4
    common_cols = list(set(left.columns).intersection(set(right.columns)))
    check_if_columns_exist(columns=common_cols, data=joined_df)

    with pytest.raises(ValueError):
        _ = auto_join(left=left, right=data)
