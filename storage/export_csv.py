import csv
import pathlib
from .save_load import CSV_DIR


def export_metadata(all_data):
    """Each page has some unique quotes. This function saves all quoutes to a csv file"""
    path = CSV_DIR / "season_metadata.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["league", "year", "title", "quote"])
        writer.writeheader()
        for league in all_data:
            for season in league["years"]:
                clean_title = season["title"].split(":", 1)[-1].strip()
                writer.writerow(
                    {
                        "league": league["league"],
                        "year": season["year"],
                        "title": clean_title,
                        "quote": season["quote"],
                    }
                )


def export_intro(all_data):
    """Each page has one h1 and some h2s. This function saves all of these and all of their <p> paragraphss to a csv file"""
    path = CSV_DIR / "intro_content.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id",
                "league",
                "year",
                "type",
                "h2_index",
                "para_index",
                "title",
                "paragraph",
            ],
        )
        writer.writeheader()

        row_id = 1
        for league in all_data:
            for season in league["years"]:
                league_name = league["league"]
                year = season["year"]
                h2_counter = 0

                for item in season["intro"]:
                    if item["type"] == "h1":
                        clean_title = item["text"]
                        if clean_title.lower().startswith("year in review :"):
                            clean_title = clean_title.split(":", 1)[-1].strip()
                        writer.writerow(
                            {
                                "id": row_id,
                                "league": league_name,
                                "year": year,
                                "type": "h1",
                                "h2_index": "",
                                "para_index": "",
                                "title": clean_title,
                                "paragraph": "",
                            }
                        )
                        row_id += 1

                    elif item["type"] == "h2":
                        h2_counter += 1
                        title = item["title"].rstrip(". ").strip()
                        for para_index, para in enumerate(item["paragraphs"], start=1):
                            writer.writerow(
                                {
                                    "id": row_id,
                                    "league": league_name,
                                    "year": year,
                                    "type": "h2",
                                    "h2_index": h2_counter,
                                    "para_index": para_index,
                                    "title": title,
                                    "paragraph": para,
                                }
                            )
                            row_id += 1


def export_table(all_data, table_key, filename):
    """Each page has some tables with hitting and pitching statistics. This function handles such tables, and saving them to disk."""
    path = CSV_DIR / filename
    all_rows = []

    for league in all_data:
        for season in league["years"]:
            league_name = league["league"]
            year = season["year"]
            tables = season.get(table_key)

            if not tables:
                continue

            # other tables is a list so if tables is a dic we can turn it into a list with 1 dict inside.
            if isinstance(tables, dict):
                tables = [tables]

            for table in tables:
                for i, row in enumerate(table["rows"], start=1):
                    row_data = {
                        "id": None,
                        "league": league_name,
                        "year": year,
                        "year_id": i,
                    }
                    row_data.update(row)
                    all_rows.append(row_data)

    if not all_rows:
        return

    all_keys = set()
    for row in all_rows:
        all_keys.update(row.keys())

    metadata_fields = ["id", "league", "year", "year_id"]
    other_fields = sorted(k for k in all_keys if k not in metadata_fields)
    fieldnames = metadata_fields + other_fields

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, row in enumerate(all_rows, start=1):
            row["id"] = i
            writer.writerow(row)


def export_to_csv(all_data):
    print("Saving CSV Files to disk.                          ", end="\r")
    export_metadata(all_data)
    export_intro(all_data)
    export_table(all_data, "hitter_table", "hitter_stats.csv")
    export_table(all_data, "pitcher_table", "pitcher_stats.csv")
    export_table(all_data, "team_review_pitcher", "team_review_pitcher.csv")
    export_table(all_data, "team_review_hitter", "team_review_hitter.csv")
    export_table(all_data, "team_standings", "team_standings.csv")
    export_table(all_data, "other_tables", "other_stats.csv")
    print("Finished Saving All CSV Files.                   ")
