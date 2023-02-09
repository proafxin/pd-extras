"""Test flatten module"""

import pandas as pd

from pandas_utils.extra.flatten import Flattener

random_nested_data = {
    "id": "0001",
    "type": "donut",
    "name": "Cake",
    "ppu": 0.55,
    "batters": {
        "batter": [
            {"id": "1001", "type": "Regular"},
            {"id": "1002", "type": "Chocolate"},
            {"id": "1003", "type": "Blueberry"},
            {"id": "1004", "type": "Devil's Food"},
        ]
    },
    "topping": [
        {"id": "5001", "type": "None"},
        {"id": "5002", "type": "Glazed"},
        {"id": "5005", "type": "Sugar"},
        {"id": "5007", "type": "Powdered Sugar"},
        {"id": "5006", "type": "Chocolate with Sprinkles"},
        {"id": "5003", "type": "Chocolate"},
        {"id": "5004", "type": "Maple"},
    ],
}


def _test_flat_data(num_rows_to_check: int, depth: int, data: pd.DataFrame) -> None:
    flattener = Flattener(num_rows_to_check=num_rows_to_check, depth=depth)

    flat_data = flattener.flatten(data=data)
    column_info = flattener.get_column_info(data=data)
    for column, status in zip(data.columns, column_info):
        if not status:
            assert column in flat_data.columns


def test_flatten_dataframe():
    """Test data flattening"""

    data = pd.DataFrame()
    data["A"] = [{"a": 1, "b": [{"c": 2, "d": [{"e": 3}]}, {"c": 4, "e": 6}]}]
    data["B"] = [[1, 2, 3]]

    _test_flat_data(num_rows_to_check=1, depth=2, data=data)

    data = pd.DataFrame(data=[random_nested_data])
    _test_flat_data(num_rows_to_check=1, depth=1, data=data)
