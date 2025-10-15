import sys
import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent.parent / "data/csv"


def clean_hitter_stats():
    path = CSV_DIR / "hitter_stats.csv"
    df = pd.read_csv(path)

    print("\nRaw Hitter Stats")
    print(df.head())
    print(f"Shape before cleaning: {df.shape}")

    # Drop duplicates
    df = df.drop_duplicates()

    # Drop rows missing critical fields
    df = df.dropna(subset=["year", "league", "Name", "Statistic", "Team"], how="any")

    # Fill optional fields
    df["Top 25"] = df["Top 25"].fillna("Top 25")
    df["guesses"] = df["guesses"].fillna("")

    # Normalize column types
    df["Statistic Value"] = pd.to_numeric(df["Statistic Value"], errors="coerce")
    df["year"] = df["year"].astype(str)

    # Strip whitespace from strings
    df["Name"] = df["Name"].str.strip()
    df["Statistic"] = df["Statistic"].str.strip()
    df["Team"] = df["Team"].str.strip()

    print(f"Shape after cleaning: {df.shape}")
    print("\nCleaned Hitter Stats")
    print(df.head())

    # Example transformation: top Doubles
    top_doubles = (
        df[df["Statistic"] == "Doubles"]
        .sort_values("Statistic Value", ascending=False)
        .head(10)
    )
    print("\nTop Doubles")
    print(top_doubles[["Name", "Team", "Statistic Value"]])

    return df


if __name__ == "__main__":
    clean_hitter_stats()
