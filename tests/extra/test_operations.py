"""Test operations module"""

import numpy as np
import pandas as pd

from pandas_utils.extra.operations import generate_random_dataframe


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
