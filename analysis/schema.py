import csv


def infer_column_types(csv_path, sample_size=50):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        samples = [row for _, row in zip(range(sample_size), reader)]

    types = {}
    for key in reader.fieldnames:
        column_values = [row[key] for row in samples]
        if all(v.isdigit() for v in column_values if v):
            types[key] = "INTEGER"
        elif all(is_float(v) for v in column_values if v):
            types[key] = "REAL"
        else:
            types[key] = "TEXT"
    return types


def is_float(value):
    try:
        float(value)
        return True
    except:
        return False
