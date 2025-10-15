import pandas as pd
from dash import Input, Output, html, dash_table
from visualisation.charts import (
    team_win_percentage_chart,
    hitter_stat_chart,
    pitcher_distribution_chart,
)


def get_filtered_data(data, league, year):
    team_df = data["team"][(data["team"]["league"] == league) & (data["team"]["year"] == year)].copy()

    # Replace empty strings with NaN so dropna works correctly
    team_df.replace("", pd.NA, inplace=True)

    # Preserve key columns even if they are all missing
    key_cols = ["Team", "Winning Percentage", "Total Wins"]
    other_cols = [col for col in team_df.columns if col not in key_cols]

    # Drop only non-key columns that are fully missing
    retained_cols = key_cols + [col for col in other_cols if not team_df[col].isna().all()]
    team_df = team_df[retained_cols]

    return {
        "intro": data["intro"][(data["intro"]["league"] == league) & (data["intro"]["year"] == year)],
        "meta": data["meta"][(data["meta"]["league"] == league) & (data["meta"]["year"] == year)],
        "hitter": data["hitter"][(data["hitter"]["league"] == league) & (data["hitter"]["year"] == year)],
        "pitcher": data["pitcher"][(data["pitcher"]["league"] == league) & (data["pitcher"]["year"] == year)],
        "team": team_df,
    }




def build_sidebar(intro_df, meta_df):
    """Construct sidebar content from intro and meta data"""
    sidebar = []

    h1_rows = intro_df[intro_df["type"] == "h1"]
    h2_rows = intro_df[intro_df["type"] == "h2"]

    for _, row in h1_rows.iterrows():
        sidebar.append(html.H2(row["title"]))

    grouped = h2_rows.groupby("title")
    for section_title, group in grouped:
        sidebar.append(html.Hr())
        sidebar.append(html.H3(section_title))
        for _, row in group.iterrows():
            sidebar.append(html.P(row["paragraph"]))

    quote_text = meta_df["quote"].dropna().values
    if len(quote_text):
        sidebar.append(html.Hr())
        sidebar.append(html.H4("Season Quote"))
        sidebar.append(html.Blockquote(
            quote_text[0],
            style={
                "fontStyle": "italic",
                "borderLeft": "4px solid #ccc",
                "paddingLeft": "1rem",
                "color": "#333",
            },
        ))

    return sidebar


def render_table(df, title, table_type="full"):
    """Render a styled Dash DataTable"""
    if df.empty:
        return html.Div(f"No data available for {title}.")

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

    return html.Div([
        html.H4(title),
        dash_table.DataTable(
            columns=columns,
            data=df.to_dict("records"),
            style_cell={"textAlign": "left", "padding": "5px"},
            style_header={"backgroundColor": "#f0f0f0", "fontWeight": "bold"},
            page_size=25,
        ),
        html.Hr(),
    ])


def build_main_content(hitter_df, pitcher_df, team_df):
    """Combine visualizations and tables into main content"""
    return html.Div([
        team_win_percentage_chart(team_df),
        # hitter_stat_chart(hitter_df),
        # pitcher_distribution_chart(pitcher_df),
        render_table(hitter_df, "Best Hitter Statistics", table_type="player"),
        render_table(pitcher_df, "Best Pitcher Statistics", table_type="player"),
        render_table(team_df, "Team Statistics"),
    ])


def update_dashboard(data, league, year):
    """Main dashboard update logic"""
    if not league or not year:
        return html.Div("Please select a league and year."), html.Div("No data available.")

    filtered = get_filtered_data(data, league, year)
    sidebar = build_sidebar(filtered["intro"], filtered["meta"])
    main_content = build_main_content(filtered["hitter"], filtered["pitcher"], filtered["team"])
    return sidebar, main_content


def register_callbacks(app, data):
    """Register all Dash callbacks"""

    @app.callback(
        Output("league-dropdown", "options"),
        Input("league-dropdown", "id")  # dummy input to trigger on load
    )
    def populate_league_options(_):
        leagues = sorted(data["team"]["league"].dropna().unique())
        return [{"label": league, "value": league} for league in leagues]

    @app.callback(
        Output("year-dropdown", "options"),
        Input("league-dropdown", "value")
    )
    def update_year_options(selected_league):
        if not selected_league:
            return []
        years = data["team"][data["team"]["league"] == selected_league]["year"].dropna().unique()
        return [{"label": str(year), "value": str(year)} for year in sorted(years)]

    @app.callback(
        Output("intro-block", "children"),
        Output("dynamic-content", "children"),
        Input("league-dropdown", "value"),
        Input("year-dropdown", "value")
    )
    def dashboard_callback(league, year):
        return update_dashboard(data, league, year)
