import pandas as pd

def top_teams_all_time(team_df, league):
    """Used to visualise the best teams of all time."""
    df = team_df[team_df["league"] == league].copy()
    df = df.groupby("Team", as_index=False)["Total Wins"].sum()
    df = df.sort_values("Total Wins", ascending=False).head(10)
    return df
