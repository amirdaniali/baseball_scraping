import pandas as pd
from dash import Input, Output, html, dash_table
from visualisation.charts import (
    team_win_percentage_chart,
    stat_trend_chart,
    top_players_chart,
    top_teams_chart,
)
from visualisation.stat_over_time import stat_trend_over_time
from visualisation.top_teams import top_teams_all_time
from visualisation.top_players_by_stat import top_players_by_stat


def get_filtered_data(data, league, year):
    team_df = data["team"][
        (data["team"]["league"] == league) & (data["team"]["year"] == year)
    ].copy()

    team_df.replace("", pd.NA, inplace=True)

    key_cols = ["Team", "Winning Percentage", "Total Wins"]
    other_cols = [col for col in team_df.columns if col not in key_cols]
    retained_cols = key_cols + [
        col for col in other_cols if not team_df[col].isna().all()
    ]
    team_df = team_df[retained_cols]

    return {
        "intro": data["intro"][
            (data["intro"]["league"] == league) & (data["intro"]["year"] == year)
        ],
        "meta": data["meta"][
            (data["meta"]["league"] == league) & (data["meta"]["year"] == year)
        ],
        "hitter": data["hitter"][
            (data["hitter"]["league"] == league) & (data["hitter"]["year"] == year)
        ],
        "pitcher": data["pitcher"][
            (data["pitcher"]["league"] == league) & (data["pitcher"]["year"] == year)
        ],
        "team": team_df,
    }


def build_sidebar(intro_df, meta_df):
    sidebar = []

    h1_rows = intro_df[intro_df["type"] == "h1"]
    h2_rows = intro_df[intro_df["type"] == "h2"]

    for _, row in h1_rows.iterrows():
        sidebar.append(
            html.H2(
                row["title"],
                id="sidebar-title",
                style={"textAlign": "center"},
            )
        )

    grouped = h2_rows.groupby("title")
    for section_title, group in grouped:
        sidebar.append(html.Hr())
        sidebar.append(
            html.H3(
                section_title,
                id=f"sidebar-info-header-{section_title}",
                style={"textAlign": "center"},
            )
        )
        for i, (_, row) in enumerate(group.iterrows()):
            sidebar.append(
                html.P(
                    row["paragraph"], id=f"sidebar-info-paragraph-{section_title}-{i}"
                )
            )

    quote_text = meta_df["quote"].dropna().values
    if len(quote_text):
        sidebar.append(html.Hr())
        sidebar.append(
            html.H4(
                "Season Quote",
                style={"textAlign": "center"},
            )
        )
        sidebar.append(
            html.Blockquote(
                quote_text[0],
                id="sidebar-quote",
                style={
                    "fontStyle": "italic",
                    "fontFamily": "Roboto Slab, Book Antiqua, Palatino, serif",
                    "fontSize": "1.3rem",
                    "borderLeft": "6px solid #ccc",
                    "paddingLeft": "1rem",
                    "color": "#333",
                },
            )
        )

    return sidebar


def render_table(df, title, table_type="full", table_id=None):
    if df.empty:
        return html.Div(f"No data available for {title}.", id=table_id)

    if table_type == "player":
        columns = [
            {"name": col, "id": col}
            for col in ["Statistic", "Team", "Name", "Statistic Value"]
        ]
    else:
        priority_cols = ["Team", "Winning Percentage"]
        filter_cols = ["Team", "Winning Percentage", "year_id", "year", "league", "id"]
        other_cols = [col for col in df.columns if col not in filter_cols]
        ordered_cols = [col for col in priority_cols if col in df.columns] + other_cols
        columns = [{"name": col, "id": col} for col in ordered_cols]

    return html.Div(
        [
            html.H4(title),
            dash_table.DataTable(
                columns=columns,
                data=df.to_dict("records"),
                style_cell={"textAlign": "left", "padding": "5px"},
                style_header={"backgroundColor": "#f0f0f0", "fontWeight": "bold"},
                page_size=25,
            ),
            html.Hr(),
        ],
        id=table_id,
    )


def build_main_content(hitter_df, pitcher_df, team_df):
    return html.Div(
        [
            html.Div(
                team_win_percentage_chart(team_df), id="team-win-percentage-chart"
            ),
            html.Div(
                render_table(
                    team_df, "Team Statistics", table_id="team-statistics-table"
                )
            ),
            html.Div(
                render_table(
                    hitter_df,
                    "Best Hitter Statistics",
                    table_type="player",
                    table_id="hitter-statistics-table",
                )
            ),
            html.Div(
                render_table(
                    pitcher_df,
                    "Best Pitcher Statistics",
                    table_type="player",
                    table_id="pitcher-statistics-table",
                )
            ),
        ]
    )


def update_dashboard(data, league, year):
    if not league or not year:
        return html.Div(
            "Please select a league and year.", id="sidebar-intro-content"
        ), html.Div("No data available.")

    filtered = get_filtered_data(data, league, year)
    sidebar = build_sidebar(filtered["intro"], filtered["meta"])
    main_content = build_main_content(
        filtered["hitter"], filtered["pitcher"], filtered["team"]
    )
    return sidebar, main_content


def register_callbacks(app, data):
    @app.callback(
        Output("league-dropdown", "options"),
        Input("league-dropdown", "id"),
    )
    def populate_league_options(_):
        leagues = sorted(data["team"]["league"].dropna().unique())
        return [{"label": league, "value": league} for league in leagues]

    @app.callback(
        Output("year-dropdown", "options"),
        Input("league-dropdown", "value"),
    )
    def update_year_options(selected_league):
        if not selected_league:
            return []
        years = (
            data["team"][data["team"]["league"] == selected_league]["year"]
            .dropna()
            .unique()
        )
        return [{"label": str(year), "value": str(year)} for year in sorted(years)]

    @app.callback(
        Output("sidebar-intro-content", "children"),
        Output("team-win-percentage-chart", "children"),
        Output("team-statistics-table", "children"),
        Output("hitter-statistics-table", "children"),
        Output("pitcher-statistics-table", "children"),
        Input("league-dropdown", "value"),
        Input("year-dropdown", "value"),
    )
    def dashboard_callback(league, year):
        sidebar, main_content = update_dashboard(data, league, year)
        return (
            sidebar,
            main_content.children[0],
            main_content.children[1],
            main_content.children[2],
            main_content.children[3],
        )

    @app.callback(
        Output("stat-select", "options"),
        Input("role-select", "value"),
    )
    def update_stat_options(role):
        df = data[role]
        stats = sorted(df["Statistic"].dropna().unique())
        return [{"label": stat, "value": stat} for stat in stats]

    @app.callback(
        Output("top-teams-all-time-chart", "children"),
        Input("league-dropdown", "value"),
    )
    def update_top_teams_chart(league):
        if not league:
            return html.Div("Please select a league.")
        team_df = top_teams_all_time(data["team"], league)
        return html.Div(
            top_teams_chart(team_df, league=league), id="chart-top-teams-all-time"
        )

    @app.callback(
        Output("historical-charts-container", "children"),
        Input("league-dropdown", "value"),
        Input("role-select", "value"),
        Input("stat-select", "value"),
    )
    def update_historical_charts(league, role, stat):
        if not league or not stat:
            return html.Div("Please select a league and statistic.")

        player_df = top_players_by_stat(data[role], league, role, stat)
        trend_df = stat_trend_over_time(data[role], league, role, stat)

        return html.Div(
            [
                html.Div(
                    top_players_chart(player_df, stat, league=league),
                    id="chart-top-players-by-stat",
                ),
                html.Div(
                    stat_trend_chart(trend_df, stat, league=league),
                    id="chart-stat-trend-over-time",
                ),
            ]
        )
