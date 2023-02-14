"""Writer for BigQuery"""


from typing import Sequence, Union

import pandas as pd
from google.api_core import page_iterator
from google.cloud import bigquery
from google.oauth2 import service_account


class BigQueryWriter:
    """BigQuery writer class"""

    def __init__(self, path_to_credentials: str) -> None:
        _credentials = service_account.Credentials.from_service_account_file(
            filename=path_to_credentials,
        )
        print(_credentials)
        self._client: bigquery.Client = bigquery.Client(credentials=_credentials)

    @property
    def project(self) -> str:
        """Get default project name

        :return: BigQuery project name
        :rtype: ```str```
        """

        return self._client.project

    def _get_dataset_ref(self, dataset_id: str):
        dataset_ref: str = f"{self.project}.{dataset_id}"

        return dataset_ref

    def _check_dataset(self, dataset_id: str):
        datasets: page_iterator.Iterator = self._client.list_datasets()
        dataset_names: list = [dataset.dataset_id for dataset in datasets]

        if dataset_id not in dataset_names:
            raise ValueError(f"{dataset_id} not in {datasets}")

    def get_dataset(self, dataset_id: str):
        """Get dataset by id

        :param dataset_id: Dataset id
        :type dataset_id: ```str```
        :return: Dataset object for ```dataset_id```
        :rtype: ```bigquery.Dataset```
        """

        self._check_dataset(dataset_id=dataset_id)
        dataset_ref = self._get_dataset_ref(dataset_id=dataset_id)

        dataset: bigquery.Dataset = self._client.get_dataset(dataset_ref=dataset_ref)

        return dataset

    def get_table_ref(self, dataset_id: str, table_name: str) -> str:
        """Get table reference for a specific table and dataset.

        :param dataset_id: Name of dataset within the default project.
        :type dataset_id: ```str```
        :param table_name: Name of table in the dataset.
        :type table_name: ```str```
        :return: The table reference string.
        :rtype: ```str```
        """

        table_id = f"{self.project}.{dataset_id}.{table_name}"

        return table_id

    def get_table(self, dataset_id: str, table_name: str) -> bigquery.Table:
        """Get specific table from a dataset within the default project.

        :param dataset_id: Dataset id of the dataset.
        :type dataset_id: ```str```
        :param table_name: Name of table.
        :type table_name: ```str```
        :raises ValueError: If ```table_name``` is not a table in the dataset.
        :return: BigQuery table object.
        :rtype: ```bigquery.Table```
        """

        table_ref = self.get_table_ref(dataset_id=dataset_id, table_name=table_name)
        dataset = self.get_dataset(dataset_id=dataset_id)
        tables = self._client.list_tables(dataset=dataset)
        table_ids = [table.table_id for table in tables]

        if table_name not in table_ids:
            raise ValueError(f"{table_name} not found in {dataset_id}")

        table = bigquery.Table(table_ref=table_ref)

        return self._client.get_table(table=table)

    def _create_table_from_dataframe(
        self,
        data: pd.DataFrame,
        table: bigquery.Table,
    ) -> bigquery.LoadJob:
        """Create a new table from a dataframe."""

        job = self._client.load_table_from_dataframe(dataframe=data, destination=table)

        return job

    def delete_all_rows(self, dataset_id: str, table_name: str) -> bigquery.QueryJob:
        """Delete all rows of the table ```table_name``` of the dataset ```dataset_id```.

        :param dataset_id: Dataset id of the dataset within the default project.
        :type dataset_id: ```str```
        :param table_name: Name of the table.
        :type table_name: ```str```
        :return: Queryjob with the deletion query.
        :rtype: ```bigquery.QueryJob```
        """

        table_ref = self.get_table_ref(dataset_id=dataset_id, table_name=table_name)
        # pylint: disable = consider-using-f-string
        query = """DELETE FROM %s WHERE true;""" % (table_ref,)

        result = self._client.query(query=query)

        return result

    def write_to_table(
        self, data: pd.DataFrame, dataset_id: str, table_name: str
    ) -> Union[bigquery.LoadJob, Sequence[Sequence[dict]]]:
        """Write a pandas dataframe to a BigQuery table.

        :param data: Pandas dataframe to be written.
        :type data: ```pd.DataFrame```
        :param dataset_id: Dataset id of the dataset within the default project.
        :type dataset_id: ```str```
        :param table_name: Name of table.
        :type table_name: ```str```
        :return: A loadjob or a sequence of dictionaries.
        :rtype: ```Union[bigquery.LoadJob, Sequence[Sequence[dict]]]```
        """

        table = self.get_table(dataset_id=dataset_id, table_name=table_name)

        schema = table.schema

        if len(schema) < 1:
            return self._create_table_from_dataframe(data=data, table=table)

        result = self._client.insert_rows_from_dataframe(table=table, dataframe=data)

        return result
