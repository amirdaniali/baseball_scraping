import argparse
import sqlite3
from pathlib import Path
from analysis.csv_importer import import_csv
from analysis.query_runner import run_query

from storage.save_load import CSV_DIR


def import_all_csvs():
    for csv_file in CSV_DIR.glob("*.csv"):
        table_name = csv_file.stem
        try:
            import_csv(csv_file, table_name)
            print(f"Imported {csv_file.name} : {table_name}")
        except Exception as e:
            print(f"Failed to import {csv_file.name}: {e}")


def import_single_csv(csv_path, table_name):
    try:
        import_csv(Path(csv_path), table_name)
        print(f"Imported {csv_path} → {table_name}")
    except Exception as e:
        print(f"Failed to import {csv_path}: {e}")


def run_sql_query(sql):
    columns, results = run_query(sql)
    print(" | ".join(columns))
    for row in results:
        print(" | ".join(str(cell) for cell in row))


def run_sql_file(path):
    try:
        sql = Path(path).read_text()
        run_sql_query(sql)
    except Exception as e:
        print(f"Failed to read SQL file {path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Baseball CLI")
    subparsers = parser.add_subparsers(dest="command")

    import_parser = subparsers.add_parser("import")
    import_parser.add_argument(
        "--all", action="store_true", help="Import all CSVs from data/csv"
    )
    import_parser.add_argument("csv_path", nargs="?", help="Path to a single CSV file")
    import_parser.add_argument(
        "table_name", nargs="?", help="Table name for single import"
    )

    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("sql", nargs="?", help="SQL query to run")
    query_parser.add_argument("--file", help="Path to SQL file")

    args = parser.parse_args()

    if args.command == "import":
        if args.all:
            import_all_csvs()
        elif args.csv_path and args.table_name:
            import_single_csv(args.csv_path, args.table_name)
        else:
            print("Provide either --all or both csv_path and table_name.")

    elif args.command == "query":
        if args.file:
            run_sql_file(args.file)
        elif args.sql:
            run_sql_query(args.sql)
        else:
            print("Provide either a SQL string or --file path to a SQL file.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
