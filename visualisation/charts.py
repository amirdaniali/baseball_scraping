import plotly.express as px
import pandas as pd
from dash import html, dcc


def team_win_percentage_chart(team_df):
    """Top 10 teams by winning percentage"""
    if team_df.empty or "Winning Percentage" not in team_df.columns:
        return html.Div("No team data available for visualization.")

    top_teams = team_df.sort_values("Winning Percentage", ascending=False).head(10)

    # Check if 'Total Wins' exists before using it
    use_text = "Total Wins" if "Total Wins" in top_teams.columns else None

    fig = px.bar(
        top_teams,
        x="Winning Percentage",
        y="Team",
        orientation="h",
        title="Top 10 Teams by Winning Percentage",
        text=use_text,
        color=use_text if use_text else "Winning Percentage",
        color_continuous_scale="Blues",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))

    return html.Div([dcc.Graph(figure=fig)])


def hitter_stat_chart(hitter_df):
    """Top hitters by statistic value"""
    if hitter_df.empty or "Statistic Value" not in hitter_df.columns:
        return html.Div("No hitter data available for visualization.")

    top_hitters = hitter_df.sort_values("Statistic Value", ascending=False).head(10)
    fig = px.bar(
        top_hitters,
        x="Statistic Value",
        y="Name",
        color="Statistic",
        title="Top 10 Hitters by Statistic Value",
        hover_data=["Team", "Statistic"],
        orientation="h",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))

    return html.Div([dcc.Graph(figure=fig)])


def pitcher_distribution_chart(pitcher_df):
    """Distribution of pitcher statistics"""
    if pitcher_df.empty or "Statistic Value" not in pitcher_df.columns:
        return html.Div("No pitcher data available for visualization.")

    fig = px.box(
        pitcher_df,
        x="Statistic",
        y="Statistic Value",
        points="all",
        title="Distribution of Pitching Statistics",
        color="Statistic",
    )

    return html.Div([dcc.Graph(figure=fig)])
