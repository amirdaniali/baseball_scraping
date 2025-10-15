import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent.parent / "data/csv"

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


def clean_team_review_hitter_pivot():
    path = CSV_DIR / "team_review_hitter.csv"
    df = pd.read_csv(path)

    # Pivot the long-form stats into wide-form
    pivot_df = df.pivot_table(
        index=["league", "year", "Team"],
        columns="Statistic",
        values="Statistic Value",
        aggfunc="first",
    ).reset_index()

    return pivot_df


if __name__ == "__main__":
    path = CSV_DIR / "team_review_hitter.csv"
    df = pd.read_csv(path)

    print("Raw Team Review Hitter")
    print(df.head())
