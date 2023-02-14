# """Test BigQuery writing"""

# import os
# from typing import Sequence

# import pandas as pd
# import pytest
# from google.cloud import bigquery
# from pd_extras.write.bq_writer import BigQueryWriter


# class TestBigQueryWriter:
#     """Test ```BigQueryWriter``` functions."""

#     _writer = BigQueryWriter(
#         path_to_credentials=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
#     )

#     def test_bq_dataset(self):
#         """Test ```get_dataset``` function."""

#         dataset = self._writer.get_dataset(dataset_id=os.environ["BIGQUERY_DATASET"])

#         assert dataset is not None
#         assert isinstance(dataset, bigquery.Dataset)

#         with pytest.raises(ValueError):
#             dataset = self._writer.get_dataset(dataset_id="2")

#     def test_bq_table(self):
#         """Test ```get_table``` function."""

#         dataset_id = os.environ["BIGQUERY_DATASET"]

#         table_name = "test__table__"

#         with pytest.raises(ValueError):
#             table = self._writer.get_table(dataset_id=dataset_id, table_name=table_name)

#         table_name = "test"

#         table = self._writer.get_table(dataset_id=dataset_id, table_name=table_name)
#         assert isinstance(table, bigquery.Table)
#         assert table.table_id == table_name
#         schema = table.schema
#         assert schema is not None
#         assert isinstance(schema, list)

#         for schema_field in schema:
#             assert isinstance(schema_field, bigquery.SchemaField)

#     def test_bq_write_to_table(self, data: pd.DataFrame):
#         """Test ```delete_all_rows``` and ```write_to_table``` functions.

#         :param data: Pandas dataframe to test, part of ```conftest.py```.
#         :type data: ```pd.DataFrame```
#         """

#         dataset_id = os.environ["BIGQUERY_DATASET"]
#         table_name = "test"

#         self._writer.delete_all_rows(dataset_id=dataset_id, table_name=table_name)

#         result = self._writer.write_to_table(
#             data=data,
#             dataset_id=dataset_id,
#             table_name=table_name,
#         )

#         assert isinstance(result, bigquery.LoadJob) or isinstance(result, Sequence)

#         result = self._writer.write_to_table(
#             data=data,
#             dataset_id=dataset_id,
#             table_name=table_name,
#         )

#         if isinstance(result, Sequence):
#             assert len(result), 0

#         self._writer.delete_all_rows(dataset_id=dataset_id, table_name=table_name)
