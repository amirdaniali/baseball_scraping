import plotly.express as px
import pandas as pd
from dash import html, dcc


def team_win_percentage_chart(team_df, year=1990):
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
        title=f"Top 10 Teams in {year}",
        text=use_text,
        color=use_text if use_text else "Winning Percentage",
        color_continuous_scale="Blues",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))

    return html.Div([dcc.Graph(figure=fig)])


def top_teams_chart(df, league):
    fig = px.bar(
        df,
        x="Total Wins",
        y="Team",
        orientation="h",
        title=f"{league} Top 10 Teams by Total Wins",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return html.Div([dcc.Graph(figure=fig)])


def top_players_chart(df, stat, league):
    fig = px.bar(
        df,
        x="Statistic Value",
        y="Name",
        color="Team",
        orientation="h",
        title=f"{league} Top 10 Players by {stat}",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    return html.Div([dcc.Graph(figure=fig)])


def stat_trend_chart(df, stat, league):
    fig = px.line(df, x="year", y="Statistic Value", title=f"{league} {stat} Over Time")
    return html.Div([dcc.Graph(figure=fig)])
