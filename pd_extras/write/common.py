"""Common variables for dataframe to database module"""

# pylint: disable=line-too-long
saved_values = {
    "sqlserver": {
        "dialect": "mssql",
        "driver": "+pymssql",
        "query": {
            "db_list": "SELECT name FROM master.sys.databases;",
            "table_list": "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='{}';",
            "column_info": "select * from information_schema.columns WHERE TABLE_CATALOG='{}' AND TABLE_SCHEMA = 'dbo' AND TABLE_NAME = '{}';",
        },
    },
    "mysql": {
        "dialect": "mysql",
        "driver": "+mysqldb",
        "query": {
            "db_list": "SHOW DATABASES;",
            "table_list": "SHOW TABLES FROM `{}`",
            "column_info": "select * from information_schema.columns WHERE table_schema='{}' and table_name='{}';",
        },
    },
    "postgresql": {
        "dialect": "postgresql",
        "driver": "+psycopg2",
        "query": {
            "db_list": "select datname from pg_database;",
            "table_list": "select * from pg_catalog.pg_tables where schemaname='{}';",
            "column_info": "select * from information_schema.columns WHERE table_catalog='{}' and table_name='{}'",
        },
    },
}
nosql_dbtypes = ["mongo"]
