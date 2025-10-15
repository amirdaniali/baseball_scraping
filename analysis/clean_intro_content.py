import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent.parent / "data/csv"


def clean_intro_content():
    """This module creates a dataframe from the intro sections. h1s are just the title of the page and have no paragraph value. h2s could have multiple paragraph values."""
    path = CSV_DIR / "intro_content.csv"
    df = pd.read_csv(path)

    print("\n--- Raw Intro Content ---")
    print(df.head())
    print(f"Initial shape: {df.shape}")

    df = df.drop_duplicates()
    df = df.dropna(subset=["year", "league", "type", "title"], how="any")

    df["paragraph"] = df["paragraph"].fillna("").str.strip()
    df["title"] = df["title"].str.strip()
    df["type"] = df["type"].str.strip()

    # Sort for readability
    df = df.sort_values(by=["year", "type", "h2_index", "para_index"])

    print(f"Cleaned shape: {df.shape}")
    print("\n--- Cleaned Intro Content ---")
    print(df.head())

    # Example: Count of entries per year
    counts = df.groupby("year")["paragraph"].count()
    print("\n--- Paragraph Count by Year ---")
    print(counts)

    return df


if __name__ == "__main__":
    clean_intro_content()
