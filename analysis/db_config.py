import sqlite3
from pathlib import Path
from storage.save_load import DATA_DIR

DB_PATH = DATA_DIR / "sqlite.db"


def get_connection() -> sqlite3.Connection:
    """returning the connection to the db"""
    return sqlite3.connect(DB_PATH)
    # I initially wanted to implement a singleton but I'm not sure if it is required or useful here.
    # All modules close the connection on their own.
