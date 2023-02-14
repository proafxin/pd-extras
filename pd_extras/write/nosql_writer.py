"""Write a pandas dataframe to a NoSQL database collection"""


import pandas as pd
import pymongo
from pd_extras.write.common import nosql_dbtypes

__all__ = ["NoSQLDatabaseWriter"]


class MongoDatabaseWriter:
    """Writer class for Mongo databases"""

    def __init__(
        self,
        host: str,
        dbname: str,
        user: str,
        password: str,
        port: int,
        dns_seed_list: bool = False,
    ) -> None:
        self._dns_seed_list = dns_seed_list

        port = int(port)
        self.__client = self._get_mongo_client(
            host=host,
            username=user,
            password=password,
            port=port,
        )
        self.__dbname: str = dbname
        self.__db = self.__client[dbname]

    def _get_mongo_client(self, host: str, username: str, password: str, port: int):
        service = "mongodb"

        if self._dns_seed_list:
            service = f"{service}+srv"
        connection_string: str = f"{service}://{username}:{password}@{host}/"

        client: pymongo.MongoClient = pymongo.MongoClient(
            host=connection_string, port=port, document_class=dict
        )

        return client

    def _get_list_of_databases(self):
        return self.__client.list_database_names()

    def _get_list_of_collections(self):
        return self.__db.list_collection_names()

    def _get_or_create_collection(self, collection_name: str):
        collection = self.__db[collection_name]

        return collection

    def _write_data_to_collection(self, data: pd.DataFrame, collection_name: str):
        collection = self._get_or_create_collection(collection_name=collection_name)
        documents = data.to_dict("records")

        res = collection.insert_many(documents=documents)

        return res

    def _get_document_count(self, collection_name: str):
        collection = self._get_or_create_collection(collection_name=collection_name)

        return collection.count_documents({})

    def _delete_collection(self, collection_name: str):
        self.__db.drop_collection(collection_name)

    def _delete_database(self):
        self.__client.drop_database(name_or_database=self.__dbname)

    def _close_connection(self):
        self.__client.close()


class NoSQLDatabaseWriter:
    """Writer class for NoSQL Database"""

    def __init__(
        self,
        dbtype: str,
        host: str,
        dbname: str,
        user: str,
        password: str,
        port: int,
        dns_seed_list: bool = False,
    ) -> None:
        if dbtype not in nosql_dbtypes:
            raise ValueError(f"{dbtype} not in {nosql_dbtypes}")

        self.__dbtype = dbtype

        self.__writer = self._get_writer(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port,
            dns_seed_list=dns_seed_list,
        )

    def _get_writer(
        self,
        host: str,
        dbname: str,
        user: str,
        password: str,
        port: int,
        dns_seed_list: bool = False,
    ):
        if self.__dbtype == "mongo":
            return MongoDatabaseWriter(
                host=host,
                dbname=dbname,
                user=user,
                password=password,
                port=port,
                dns_seed_list=dns_seed_list,
            )

        return None

    def get_list_of_databases(self):
        """List names of databses in this connection.

        :return: Database names.
        :rtype: `list[str]`
        """

        return self.__writer._get_list_of_databases()

    def get_list_of_collections(self):
        """List names of collections in the current database.

        :return: Collection names.
        :rtype: `list[str]`
        """

        return self.__writer._get_list_of_collections()

    def get_or_create_collection(self, collection_name: str):
        """Get object for the collection `collection_name`.

        :param collection_name: Name of the collection.
        :type collection_name: `str`
        :return: Collection object.
        :rtype: `pymongo.collection.Collection`
        """

        return self.__writer._get_or_create_collection(collection_name=collection_name)

    def write_data_to_collection(self, collection_name: str, data: pd.DataFrame):
        """Write dataframe `data` to the collection `collection_name`.

        :param collection_name: Name of the collection.
        :type collection_name: `str`
        :param data: Dataframe to write.
        :type data: `pd.DataFrame`
        :return: Object with ids of inserted documents.
        :rtype: `pymongo.results.InsertManyResult`
        """

        return self.__writer._write_data_to_collection(
            collection_name=collection_name, data=data
        )

    def get_document_count(self, collection_name: str):
        """Get number of documents in collection `collection_name`.

        :param collection_name: Name of the collection.
        :type collection_name: `str`
        :return: Document count.
        :rtype: `int`
        """

        return self.__writer._get_document_count(collection_name=collection_name)

    def delete_collection(self, collection_name: str):
        """Delete collection `collection_name`.

        :param collection_name: Name of the collection.
        :type collection_name: `str`
        """

        self.__writer._delete_collection(collection_name=collection_name)

    def delete_database(self):
        """Drop the current database."""

        self.__writer._delete_database()

    def close_connection(self):
        """Close the current connection."""

        self.__writer._close_connection()
