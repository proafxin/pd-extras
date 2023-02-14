"""Write a pandas dataframe to a SQL database table"""


import pandas as pd
from pandas.api.types import is_integer_dtype, is_numeric_dtype  # type: ignore
from pd_extras.write.common import saved_values
from sqlalchemy import (
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    text,
)
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists


class SQLDatabaseWriter:
    """Database connection object for SQL databases
    Only database name `dbname` is stored.
    Rest of the credentials are used only to retrieved the connection.
    Two connections are created: one for the specific database `dbname`
    and another generic connection with no database selected.
    Be sure to call `connobj.close_connection()` after you are done.
    """

    def __init__(
        self,
        dbtype: str,
        host: str,
        dbname: str,
        user: str,
        password: str,
        port: int,
    ):
        assert dbtype in saved_values, f"{dbtype} not in {list(saved_values.keys())}"
        assert dbname is not None, "`dbname` must be a valid database name"
        self.__dbtype = dbtype
        self.__dbname = dbname
        port = int(port)

        self.__engine = self._get_db_specific_engine(
            host=host,
            user=user,
            password=password,
            port=port,
        )

        if not database_exists(url=self.__engine.url):
            create_database(self.__engine.url)

    def _get_db_specific_engine(self, host: str, user: str, password: str, port: int):
        dialect = saved_values[self.__dbtype]["dialect"]
        driver = saved_values[self.__dbtype]["driver"]

        connection_string = (
            f"{dialect}{driver}://{user}:{password}@{host}:{port}/{self.__dbname}"
        )

        engine = create_engine(connection_string, future=True)

        return engine

    def get_data_from_query(self, query: str):
        """Execute a single query on the current database.

        :param query: SQL statement to execute.
        :type query: `str`
        :return: Pandas dataframe with result of query.
        :rtype: `pd.DataFrame`
        """

        with self.__engine.connect() as conn:
            return pd.read_sql(sql=text(query), con=conn)

    def get_list_of_database(self):
        """Get list of databases.

        :return: List containing database names.
        :rtype: `list[str]`
        """

        query = saved_values[self.__dbtype]["query"]["db_list"]

        res = self.get_data_from_query(query=query)
        database_names = res[res.columns[0]].to_numpy()

        return database_names

    def get_column_info(self, table_name: str):
        """Get table schema from database.

        :param table_name: Name of the table in database.
        :type table_name: ``str``
        :return: Pandas dataframe of table schema information.
        :rtype: ``pd.DataFrame``
        """

        sa_session = Session(self.__engine)
        _saved_values: dict = saved_values[self.__dbtype]

        self._check_name(name=self.__dbname)
        self._check_name(name=table_name)

        query: str = _saved_values["query"]["column_info"] % (
            self.__dbname,
            table_name,
        )
        session = sa_session.execute(query)
        cursor = session.cursor  # type: ignore
        cols = [detail[0] for detail in cursor.description]
        res = cursor.fetchall()
        res = [list(row) for row in res]

        info = pd.DataFrame(res, columns=cols)
        columns: list = [str(column.lower()) for column in info.columns.tolist()]
        info.columns = columns  # type: ignore

        session.close()

        return info

    def has_table(self, table_name: str):
        """Check if the current database has table `table_name`.

        :param table_name: Name of the table to check.
        :type table_name: `str`
        :return: True if `table_name` exists in current database.
        :rtype: `bool`
        """

        with self.__engine.connect() as connection:
            if "server" in self.__dbtype:
                return self.__engine.dialect.has_table(
                    connection=connection, tablename=table_name
                )
            else:
                return self.__engine.dialect.has_table(
                    connection=connection, table_name=table_name
                )

    def _check_null(self, data: pd.DataFrame, info: pd.DataFrame, id_col: str):
        columns = info["column_name"].to_numpy()
        nullable_status = info["is_nullable"].to_numpy()

        columns_valid = []
        for column, status in zip(columns, nullable_status):
            if id_col == column:
                continue
            if column not in data.columns:
                raise ValueError(f"{column} not in columns: {data.columns.tolist()}")

            if status.lower() == "no":
                if data[column].dropna().shape[0] < data.shape[0]:
                    raise ValueError(f"`{column}` is non-nullable but has null value")
            columns_valid.append(column)

        data = data[columns_valid].copy()
        data = data.reset_index(drop=True)

        return data

    def _check_name(self, name: str) -> None:
        for char in name:
            if (not char.isalnum()) and (char not in ["_", "-"]):
                raise ValueError(f"Unacceptable character {char} found in {name}")

    def _clean_column(self, column: str):
        return str(column).strip().strip('"')

    def _clean_columns(self, data: pd.DataFrame):
        data.columns = [self._clean_column(column) for column in data.columns]  # type: ignore

        return data

    def _get_table_from_dataframe(
        self,
        data: pd.DataFrame,
        table_name: str,
        id_col: str,
        max_length: int = 100,
    ):
        metadata = MetaData(self.__engine)
        columns = []

        if id_col:
            columns.append(Column(id_col, Integer, primary_key=True, nullable=False))

        for column in data.columns:
            nullable_status = False
            if data[column].dropna().shape[0] < data.shape[0]:
                nullable_status = True

            if is_integer_dtype(data[column]):
                columns.append(Column(column, Integer, nullable=nullable_status))
            elif is_numeric_dtype(data[column]):
                columns.append(Column(column, Float, nullable=nullable_status))
            else:
                columns.append(
                    Column(column, String(max_length), nullable=nullable_status)
                )

        table = Table(table_name, metadata, *columns)

        return table

    def _create_new_table(self, table: Table):
        table.create(bind=self.__engine, checkfirst=True)

        return table

    def _write_data_to_table(self, data: pd.DataFrame, table: Table):
        records = data.to_dict("records")

        with self.__engine.connect() as conn:
            ins = table.insert()

            result = conn.execute(ins, records)
            conn.commit()

            return result

    def delete_table(self, table_name: str):
        """Drop table `table_name` from the current database if it exists.

        :param table: Table to delete.
        :type table: `Table`
        """

        query = f"DROP TABLE IF EXISTS {table_name}"
        with self.__engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()

    def write_df_to_db(
        self,
        data: pd.DataFrame,
        table_name: str,
        id_col: str = "id",
        drop_first: bool = False,
        clean_columns: bool = True,
        max_length: int = 100,
    ):
        """Write `data` to Table `table_name`

        :param data: Pandas dataframe containing data to write.
        :type data: `pd.DataFrame`
        :param dbname: Name of the database.
        :type dbname: `str`
        :param table_name: Name of table in the database.
        :type table_name: `str`
        :param id_col: Id column of table if exists, defaults to "id".
            Should be set to `None` if not present in data.
        :type id_col: `str`, optional
        :param drop_first: If True, table `table_name` in database will be attempted to drop first.
        :type drop_first: `bool`
        :param clean_columns: If True, trailing/leading whitespaces and " will be stripped
            off column names, defaults to "True".
        :type clean_columns: `bool`
        :param max_length: Maximum length of VARCHAR type columns, defaults to 100.
        :type max_length: `int`
        :return: Cursor with result of query execution.
        :rtype: `sqlalchemy.engine.cursor.CursorResult`
        """

        if id_col and len(id_col) > 0 and (id_col in data.columns):
            data = data.drop(id_col, axis=1)

        if clean_columns:
            data = self._clean_columns(data=data)

        data = data.astype(object).where(pd.notnull(data), None)  # type: ignore

        table = self._get_table_from_dataframe(
            data=data,
            table_name=table_name,
            id_col=id_col,
            max_length=max_length,
        )

        if drop_first:
            self.delete_table(table_name=table_name)

        table = self._create_new_table(table=table)
        info = self.get_column_info(table_name=table_name)
        data = self._check_null(data=data, info=info, id_col=id_col)
        result = self._write_data_to_table(data=data, table=table)

        return result

    def close_connection(self):
        """Close the current connection to the database"""

        self.__engine.dispose()
