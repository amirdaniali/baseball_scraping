import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent.parent / "data/csv"


def clean_other_stats():
    path = CSV_DIR / "other_stats.csv"
    df = pd.read_csv(path)

    print("\nRaw Other Stats")
    print(df.head())
    print(f"Initial shape: {df.shape}")

    df = df.drop_duplicates()
    df = df.dropna(subset=["year", "league", "Team"], how="any")

    # Normalize Payroll
    df["Payroll"] = df["Payroll"].replace("[\\$,]", "", regex=True)
    df["Payroll"] = pd.to_numeric(df["Payroll"], errors="coerce").fillna(0)

    # Normalize other numeric columns
    numeric_cols = ["Games Behind", "Total Wins", "Total Loses", "Winning Percentage"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["Team"] = df["Team"].str.strip()
    df["division"] = df["division"].fillna("").str.strip()

    print(f"Cleaned shape: {df.shape}")
    print("\nCleaned Other Stats")
    print(df.head())

    # Example: Top payrolls
    top_payroll = df.sort_values("Payroll", ascending=False).head(10)
    print("\nTop Payrolls")
    print(top_payroll[["Team", "Payroll", "Winning Percentage"]])

    return df


if __name__ == "__main__":
    clean_other_stats()
