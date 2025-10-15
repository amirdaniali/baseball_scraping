import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent.parent / "data/csv"

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


def clean_team_review_pitcher():
    """The team review tables aren't as common on the website. most of the entries don't have those tables or have just some columns. as such, aggressive dropna()s will remove most of the useful data."""

    path = CSV_DIR / "team_review_pitcher.csv"
    df = pd.read_csv(path)
    print(df.head())

    # Normalize strings
    df["Team"] = df["Team"].str.strip()
    df["Statistic"] = df["Statistic"].str.strip()

    # Example: Total Strikeouts by Team

    df["Total Strikeouts"] = pd.to_numeric(
        df["Total Strikeouts"], errors="coerce"
    ).fillna(0)

    strikeouts_by_team = (
        df.groupby("Team")["Total Strikeouts"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    print("\nTop Teams by Total Strikeouts")
    print(strikeouts_by_team)

    return df


if __name__ == "__main__":
    clean_team_review_pitcher()
