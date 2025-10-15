import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent.parent / "data/csv"


def clean_intro_content():
    """This module creates a dataframe from the intro sections. h1s are just the title of the page and have no paragraph value. h2s could have multiple paragraph values."""
    path = CSV_DIR / "intro_content.csv"
    df = pd.read_csv(path)

    df.columns = df.columns.str.strip()
    df["league"] = df["league"].astype(str).str.strip()
    df["year"] = df["year"].astype(str).str.strip()
    df["type"] = df["type"].astype(str).str.strip()
    df["title"] = df["title"].fillna("").astype(str).str.strip()
    df["paragraph"] = df["paragraph"].fillna("").astype(str).str.strip()

    return df


if __name__ == "__main__":
    path = CSV_DIR / "intro_content.csv"
    df = pd.read_csv(path)

    print("\n--- Raw Intro Content ---")
    print(df.head())
    print(f"Initial shape: {df.shape}")

    df = clean_intro_content()
    counts = df.groupby("year")["paragraph"].count()

    # Example: Count of entries per year
    print("\nParagraph Count by Year")
    print(counts)
