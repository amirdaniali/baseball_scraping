import csv
import sqlite3
from .db_config import get_connection
from .schema import infer_column_types


def import_csv(csv_path, table_name):
    conn = get_connection()
    cursor = conn.cursor()

    column_types = infer_column_types(csv_path)
    columns_sql = ", ".join([f'"{col}" {dtype}' for col, dtype in column_types.items()])
    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    cursor.execute(f'CREATE TABLE "{table_name}" ({columns_sql})')

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [tuple(row[col] for col in reader.fieldnames) for row in reader]
        placeholders = ", ".join(["?"] * len(reader.fieldnames))
        cursor.executemany(f'INSERT INTO "{table_name}" VALUES ({placeholders})', rows)

    conn.commit()
    conn.close()
