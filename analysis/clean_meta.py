import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent.parent / "data/csv"


def clean_meta():
    path = CSV_DIR / "season_metadata.csv"
    df = pd.read_csv(path)

    # Normalize column names
    df.columns = df.columns.str.strip()

    # Ensure league and year are strings
    df["league"] = df["league"].astype(str).str.strip()
    df["year"] = df["year"].astype(str).str.strip()

    # Clean quote column if present
    if "quote" in df.columns:
        df["quote"] = df["quote"].fillna("").astype(str).str.strip()

    # Drop rows missing league or year
    df = df.dropna(subset=["league", "year"])

    return df


if __name__ == "__main__":
    meta_df = clean_meta()
    print("Cleaned meta data:")
    print(meta_df.head())
    print(f"Total rows: {len(meta_df)}")
    print(f"Leagues: {meta_df['league'].unique()}")
    print(f"Years: {meta_df['year'].unique()}")
