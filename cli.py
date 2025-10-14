import argparse
import sqlite3
from pathlib import Path
from analysis.csv_importer import import_csv
from analysis.query_runner import run_query

from analysis.demo_queries import (
    demo_top_hitters,
    demo_pitcher_team_review,
    demo_intro_by_year,
    demo_metadata_summary,
)


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
    query_parser.add_argument("sql", help="SQL query to run")

    demo_parser = subparsers.add_parser("demo", help="Run predefined demo queries")
    demo_parser.add_argument(
        "name",
        choices=["top_hitters", "pitcher_review", "intro_year", "metadata"],
        help="Name of the demo to run",
    )
    demo_parser.add_argument(
        "--year",
        default="1882",
        help="Year filter for intro content (used with intro_year demo)",
    )

    args = parser.parse_args()

    if args.command == "import":
        if args.all:
            import_all_csvs()
        elif args.csv_path and args.table_name:
            import_single_csv(args.csv_path, args.table_name)
        else:
            print("Provide either --all or both csv_path and table_name.")
    elif args.command == "query":
        run_sql_query(args.sql)
    elif args.command == "demo":
        if args.name == "top_hitters":
            demo_top_hitters()
        elif args.name == "pitcher_review":
            demo_pitcher_team_review()
        elif args.name == "intro_year":
            demo_intro_by_year(args.year)
        elif args.name == "metadata":
            demo_metadata_summary()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
