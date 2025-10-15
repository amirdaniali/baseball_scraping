import csv
import re
from datetime import datetime


def is_integer(value) -> bool:
    return re.fullmatch(r"-?\d+", value) is not None


def is_float(value) -> bool:
    return re.fullmatch(r"-?\d*\.\d+", value) is not None or is_integer(value)


def is_boolean(value) -> bool:
    return value.lower() in {"true", "false", "1", "0"}


def is_date(value) -> bool:
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            datetime.strptime(value, fmt)
            return True
        except ValueError:
            continue
    return False


def infer_column_types(csv_path, sample_size=250):
    """Dynamcially sample some rows in the csv file and determine the column type from the sample data"""
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        samples = [row for _, row in zip(range(sample_size), reader)]

    types = {}
    for key in reader.fieldnames:
        column_values = [row[key].strip() for row in samples if row[key].strip()]

        if not column_values:
            types[key] = "TEXT"
            continue

        if all(is_boolean(v) for v in column_values):
            types[key] = "BOOLEAN"
        elif all(is_date(v) for v in column_values):
            types[key] = "DATE"
        elif all(is_integer(v) for v in column_values):
            types[key] = "INTEGER"
        elif all(is_float(v) for v in column_values):
            types[key] = "REAL"
        else:
            types[key] = "TEXT"

    return types
