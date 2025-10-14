import sqlite3
from pathlib import Path
from storage.save_load import DATA_DIR

DB_PATH = DATA_DIR / "sqlite.db"


def get_connection():
    return sqlite3.connect(DB_PATH)
