import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent.parent / "data/csv"

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


def clean_team_standings():
    """The team standings table isn't as common on the website. most of the entries don't have the table or have just some columns. as such, aggressive dropna()s will remove most of the useful data."""

    path = CSV_DIR / "team_standings.csv"
    df = pd.read_csv(path)

    print("\nRaw Team Standings")
    print(df.head())
    print(f"Initial shape: {df.shape}")

    df = df.drop_duplicates()
    df = df.dropna(subset=["year", "league", "Team"], how="any")

    # Normalize numeric columns
    numeric_cols = [
        "Total Wins",
        "Total Loses",
        "Total Ties",
        "Games Behind",
        "Winning Percentage",
        "Wins",
        "Losses",
        "Ties",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Team"] = df["Team"].str.strip()
    df["division"] = df["division"].fillna("").str.strip()

    print(f"Cleaned shape: {df.shape}")
    print("\nCleaned Team Standings")
    print(df.head())

    # Example: Top teams by win percentage
    top_wp = df.sort_values("Winning Percentage", ascending=False).head(10)
    print("\nTop Teams by Win %")
    print(top_wp[["Team", "Winning Percentage", "division"]])

    return df


if __name__ == "__main__":
    clean_team_standings()
