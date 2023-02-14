"""Test NoSQLDatabaseWriter Class"""

import os

import pandas as pd
from pd_extras.write.nosql_writer import NoSQLDatabaseWriter
from pymongo import results

DBNAME = "_testdb_"

print(os.environ['MONGO_PORT'])
print(type(os.environ['MONGO_PORT']), int(os.environ['MONGO_PORT']))

MONGO_CONNECTION = NoSQLDatabaseWriter(
    dbtype="mongo",
    host=os.environ["MONGO_HOST"],
    dbname=DBNAME,
    user=os.environ["MONGO_USER"],
    password=os.environ["MONGO_PASSWORD"],
    port=int(os.environ["MONGO_PORT"]),
    dns_seed_list=True,
)

# LOCALHOST_CONN = NoSQLDatabaseWriter(
#     dbtype="mongo",
#     host=os.environ["LOCAL_MONGO_HOST"],
#     dbname=DBNAME,
#     user=os.environ["LOCAL_MONGO_USER"],
#     password=os.environ["LOCAL_MONGO_PASSWORD"],
#     port=int(os.environ["MONGO_PORT"]),
#     dns_seed_list=False,
# )

CONNECTIONS = (("mongo", {"conn": MONGO_CONNECTION}),)


def pytest_generate_tests(metafunc):
    """Generate pytest Tests for all connections

    :param metafunc: _description_
    :type metafunc: _type_
    """

    idlist = []
    argvalues = []
    for scenario in metafunc.cls.connections:
        idlist.append(scenario[0])
        items = scenario[1].items()
        argnames = [x[0] for x in items]
        argvalues.append([x[1] for x in items])
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


class TestNoSQLDatabaseWriter:
    """Test class for NoSQLDatabaseWriter"""

    connections = CONNECTIONS

    def _test_connection(self, conn: NoSQLDatabaseWriter):
        database_names = conn.get_list_of_databases()
        assert DBNAME in database_names

        assert isinstance(database_names, list)
        for database_name in database_names:
            assert isinstance(database_name, str)

    def test_write_to_collection(
        self,
        conn: NoSQLDatabaseWriter,
        data: pd.DataFrame,
    ):
        """Test writing data to collections."""

        collection_name = "_test_collection_"

        count_initial = conn.get_document_count(collection_name=collection_name)

        res = conn.write_data_to_collection(collection_name=collection_name, data=data)
        assert isinstance(res, results.InsertManyResult)

        self._test_connection(conn=conn)

        inserted_ids = res.inserted_ids
        assert isinstance(inserted_ids, list)

        count_new = conn.get_document_count(collection_name=collection_name)
        assert len(inserted_ids) == count_new - count_initial
        assert len(inserted_ids) == data.shape[0]

        collection_names = conn.get_list_of_collections()
        assert collection_name in collection_names

    def test_delete_collection(self, conn: NoSQLDatabaseWriter):
        """Test collection dropping."""

        collection_name = "_test_collection_"
        conn.delete_collection(collection_name=collection_name)
        collection_names = conn.get_list_of_collections()
        assert collection_name not in collection_names

    def test_drop_database(self, conn: NoSQLDatabaseWriter):
        """Test dropping database."""

        database_names = conn.get_list_of_databases()
        assert DBNAME not in database_names
        conn.close_connection()
