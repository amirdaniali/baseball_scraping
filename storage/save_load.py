import json
import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CSV_DIR = DATA_DIR / "csv"
JSON_DIR = DATA_DIR / "json"

DATA_DIR.mkdir(exist_ok=True)
CSV_DIR.mkdir(exist_ok=True)
JSON_DIR.mkdir(exist_ok=True)


def save_year_data(league: str, year: str, data: dict):
    """Gets the league and year and stores the data as json to memory"""
    league_dir = JSON_DIR / league
    league_dir.mkdir(exist_ok=True)
    path = league_dir / f"{year}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_all_data():
    """Loads all scraped data stored on disk to avoid rescraping."""
    all_data = []
    for league_dir in JSON_DIR.iterdir():
        if league_dir.is_dir():
            league_record = {"league": league_dir.name, "years": []}
            for year_file in league_dir.glob("*.json"):
                with year_file.open(encoding="utf-8") as f:
                    year_data = json.load(f)
                    league_record["years"].append(year_data)
            all_data.append(league_record)
    return all_data


def get_saved_year_path(league: str, year: str) -> pathlib.Path:
    "Handles the creation of league directories and file saving."
    league_dir = JSON_DIR / league
    league_dir.mkdir(parents=True, exist_ok=True)
    return league_dir / f"{year}.json"


def is_year_saved(league: str, year: str) -> bool:
    """Small function to determine if a certain league and year data is already present on disk. If not we will have to scrap it."""
    return get_saved_year_path(league, year).exists()
