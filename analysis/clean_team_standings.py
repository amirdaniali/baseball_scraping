import pandas as pd
from pathlib import Path

CSV_DIR = Path(__file__).parent.parent / "data/csv"

def cleaner(value):
    if isinstance(value, str):
        value = value.replace('½', '.5').replace(",", "").replace('"', "").strip()
        try:
            return pd.to_numeric(value, errors='coerce')
        except:
            return None
    return value

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

def clean_team_standings():
    path = CSV_DIR / "team_standings.csv"
    df = pd.read_csv(path)

    # Drop duplicates and rows missing critical identifiers
    df = df.drop_duplicates()
    df = df.dropna(subset=["year", "league", "Team"], how="any")

    # Normalize column names (strip whitespace)
    
    df.columns = [col.strip() for col in df.columns]

    # Fix common column name typo if present
    if "Total Loses" in df.columns:
        df.rename(columns={"Total Loses": "Total Losses"}, inplace=True)


    # Clean numeric columns
    numeric_cols = [
        "Total Wins",
        "Total Losses",
        "Total Ties",
        "Games Behind",
        "Winning Percentage",
        "Payroll",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].apply(cleaner)

    # Add Total Games column
    if all(col in df.columns for col in ["Total Wins", "Total Losses"]):
        df["Total Games"] = df["Total Wins"].fillna(0) + df["Total Losses"].fillna(0)
        if "Total Ties" in df.columns:
            df["Total Games"] += df["Total Ties"].fillna(0)

    # Clean string columns
    df["Team"] = df["Team"].astype(str).str.strip()
    df["year"] = df["year"].astype(str)
    df["league"] = df["league"].astype(str).str.strip()

    # Fill missing 'Games Behind' with 0
    if "Games Behind" in df.columns:
        df["Games Behind"] = df["Games Behind"].fillna(0)

    return df
