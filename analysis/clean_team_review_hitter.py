import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent.parent / "data/csv"

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


def clean_team_review_hitter():
    """The team review tables aren't as common on the website. most of the entries don't have those tables or have just some columns. as such, aggressive dropna()s will remove most of the useful data."""
    path = CSV_DIR / "team_review_hitter.csv"
    df = pd.read_csv(path)

    return df


if __name__ == "__main__":
    path = CSV_DIR / "team_review_hitter.csv"
    df = pd.read_csv(path)

    print("Raw Team Review Hitter")
    print(df.head())
    df = clean_team_review_hitter()
    games_by_team = (
        df.groupby("Team")["Total Games"].sum().sort_values(ascending=False).head(10)
    )
    print("\nTop Teams by Total Games Played")
    print(games_by_team)
