import argparse
from analysis.csv_importer import import_csv
from analysis.query_runner import run_query


def main():
    parser = argparse.ArgumentParser(description="Season Data CLI")
    subparsers = parser.add_subparsers(dest="command")

    import_parser = subparsers.add_parser("import")
    import_parser.add_argument("csv_path", help="Path to CSV file")
    import_parser.add_argument("table_name", help="Name of the table")

    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("sql", help="SQL query to run")

    args = parser.parse_args()

    if args.command == "import":
        import_csv(args.csv_path, args.table_name)
        print(f"Imported {args.csv_path} into table {args.table_name}")
    elif args.command == "query":
        columns, results = run_query(args.sql)
        print(" | ".join(columns))
        for row in results:
            print(" | ".join(str(cell) for cell in row))


if __name__ == "__main__":
    main()
