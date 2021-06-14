"""
Utilities for updating and modifying database data.
"""

import os
import csv
import sqlite3

from typing import Tuple


def get_conn(db_name: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Opens and returns a connection to a database.
    """
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()


def close_conn(conn: sqlite3.Connection) -> None:
    """
    Commits and closes a database connection.
    """
    conn.commit()
    conn.close()


def drop_database(database: str) -> None:
    """
    Clears the specified database.
    """
    if os.path.exists(database):
        os.remove(database)


if __name__ == '__main__':
    pass
