import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent.parent / "data/csv"

import pandas as pd
import re
from fractions import Fraction

def cleaner(value):
    if isinstance(value, str):
        # Replace "½" with ".5" and try converting
        value = value.replace('½', '.5')
        value = value.replace(",", "").strip()
        value = value.replace('"', "").strip()
        try:
            return pd.to_numeric(value, errors='coerce')
        except:
            return None



pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


def clean_team_standings():
    """The team standings table isn't as common on the website. most of the entries don't have the table or have just some columns. as such, aggressive dropna()s will remove most of the useful data."""

    path = CSV_DIR / "team_standings.csv"
    df = pd.read_csv(path)

    df = df.drop_duplicates()
    df = df.dropna(subset=["year", "league", "Team"], how="any")
    

    # Normalize numeric columns
    # Apply to your DataFrame column
    try:
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
                df[col] = df[col].apply(cleaner)
    except ValueError as e:
        print(f"error: {col}, ", e)

    df["year"] = df["year"].astype(str)
    df["Games Behind"] = df["Games Behind"].fillna(0)

    # Strip whitespace from strings

    df["Team"] = df["Team"].str.strip()


    return df


if __name__ == "__main__":
    path = CSV_DIR / "team_standings.csv"
    df = pd.read_csv(path)

    print("\nRaw Team Standings")
    print(df.head())
    print(f"Initial shape: {df.shape}")

    df = clean_team_standings()
    
    print(f"Cleaned shape: {df.shape}")
    print("\nCleaned Team Standings")
    print(df.head())

    # Example: Top teams by win percentage
    top_wp = df.sort_values("Winning Percentage", ascending=False).head(10)
    print("\nTop Teams by Win %")
    print(top_wp[["Team", "Winning Percentage", "Division"]])