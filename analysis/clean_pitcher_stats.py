import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent.parent / "data/csv"


def clean_pitcher_stats():
    path = CSV_DIR / "pitcher_stats.csv"
    df = pd.read_csv(path)

    print("\nRaw Pitcher Stats")
    print(df.head())
    print(f"Initial shape: {df.shape}")

    # Drop duplicates
    df = df.drop_duplicates()

    # Drop rows missing critical fields
    df = df.dropna(subset=["year", "league", "Name", "Statistic", "Team"], how="any")

    # Normalize Statistic Value to numeric
    df["Statistic Value"] = pd.to_numeric(df["Statistic Value"], errors="coerce")

    # Fill optional fields
    df["Top 25"] = df["Top 25"].fillna("")

    # Strip whitespace
    df["Name"] = df["Name"].str.strip()
    df["Statistic"] = df["Statistic"].str.strip()
    df["Team"] = df["Team"].str.strip()

    print(f"Cleaned shape: {df.shape}")
    print("\nCleaned Pitcher Stats")
    print(df.head())

    # Example: Top Complete Games
    top_cg = (
        df[df["Statistic"] == "Complete Games"]
        .sort_values("Statistic Value", ascending=False)
        .head(10)
    )
    print("\nTop Complete Games")
    print(top_cg[["Name", "Team", "Statistic Value"]])

    return df


if __name__ == "__main__":
    clean_pitcher_stats()
