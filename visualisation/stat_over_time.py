def stat_trend_over_time(df, league, role, stat):
    """used to visualize the the trend thoughtout history."""
    df = df[df["league"] == league]
    df = df[df["Statistic"] == stat]
    df = df.groupby("year", as_index=False)["Statistic Value"].mean()
    df["year"] = df["year"].astype(int)
    return df.sort_values("year")