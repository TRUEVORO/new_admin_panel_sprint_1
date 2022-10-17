import os
import sqlite3
from contextlib import closing, contextmanager

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from pg_saver import PostgresSaver
from sqlite_extr import SQLiteExtractor


@contextmanager
def conn_sqlite(db_path: str):
    """Контекстный менеджер для закрытия соединения SQLite."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_connection: _connection) -> None:
    """Основной метод загрузки данных из SQLite в Postgres."""
    postgres_saver = PostgresSaver(pg_connection)
    sqlite_extractor = SQLiteExtractor(connection)

    data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':

    load_dotenv(r'../movies_admin/config/.env')

    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432),
    }

    with conn_sqlite(os.environ.get('SQLITE_PATH')) as sqlite_conn, closing(
            psycopg2.connect(**dsl, cursor_factory=DictCursor),
    ) as pg_conn:

        load_from_sqlite(sqlite_conn, pg_conn)
