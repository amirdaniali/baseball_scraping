
import pandas as pd

def top_players_by_stat(df, league, role, stat):
    """Used to visualize the best players for a stat"""
    df = df[df["league"] == league]
    if role == "hitter":
        df = df[df["Statistic"].isin(df["Statistic"].unique()) & (df["Statistic"] == stat)]
    elif role == "pitcher":
        df = df[df["Statistic"].isin(df["Statistic"].unique()) & (df["Statistic"] == stat)]
    df = df.sort_values("Statistic Value", ascending=False).head(10)
    return df