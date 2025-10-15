from dash import Input, Output, html, dash_table
from visualisation.data_loader import load_all_data

data = load_all_data()


def update_dashboard(league, year):
    if not league or not year:
        return html.Div("Please select a league and year."), html.Div("No data available.")

    intro = data["intro"]
    meta = data["meta"]
    hitter = data["hitter"]
    pitcher = data["pitcher"]
    team = data["team"]

    # Sidebar content
    intro_texts = intro[(intro["league"] == league) & (intro["year"] == year)]
    h1_rows = intro_texts[intro_texts["type"] == "h1"]
    h2_rows = intro_texts[intro_texts["type"] == "h2"]
    meta_df = meta[(meta["league"] == league) & (meta["year"] == year)]
    hitter_df = hitter[(hitter["league"] == league) & (hitter["year"] == year)]
    pitcher_df = pitcher[(pitcher["league"] == league) & (pitcher["year"] == year)]
    team_df = team[(team["league"] == league) & (team["year"] == year)]
    team_df = team_df.dropna(axis=1, how="all")

    sidebar = []
    for _, row in h1_rows.iterrows():
        sidebar.append(html.H2(row["title"]))
    grouped = h2_rows.groupby("title")
    for section_title, group in grouped:
        sidebar.append(html.Hr())
        sidebar.append(html.H3(section_title))
        for _, row in group.iterrows():
            sidebar.append(html.P(row["paragraph"]))

    quote_text = meta_df["quote"].dropna().values
    quote_block = html.Div(
        [
            html.Hr(),
            html.H4("Season Quote"),
            html.Blockquote(
                quote_text[0] if len(quote_text) else "No quote available.",
                style={
                    "fontStyle": "italic",
                    "borderLeft": "4px solid #ccc",
                    "paddingLeft": "1rem",
                    "color": "#333",
                },
            ),
        ]
    )
    sidebar.append(quote_block)

    # Table rendering
    def render_table(df, title, table_type="full"):
        if df.empty:
            return html.Div(f"No data available for {title}.")
        if table_type == "player":
            return html.Div(
                [
                    html.H4(title),
                    dash_table.DataTable(
                        columns=[
                            {"name": col, "id": col}
                            for col in ["Statistic", "Team", "Name", "Statistic Value"]
                        ],
                        data=df.to_dict("records"),
                        style_table={"overflowX": "auto"},
                        style_cell={"textAlign": "left", "padding": "5px"},
                        style_header={"backgroundColor": "#f0f0f0", "fontWeight": "bold"},
                        page_size=25,
                    ),
                    html.Hr(),
                ]
            )

        priority_cols = ["Team", "Winning Percentage"]
        filter_cols = ["Team", "Winning Percentage", "year_id", "year", "league", "id"]
        other_cols = [col for col in df.columns if col not in filter_cols]
        ordered_cols = [col for col in priority_cols if col in df.columns] + other_cols

        return html.Div(
            [
                html.H4(title),
                dash_table.DataTable(
                    columns=[{"name": col, "id": col} for col in ordered_cols],
                    data=df.to_dict("records"),
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left", "padding": "5px"},
                    style_header={"backgroundColor": "#f0f0f0", "fontWeight": "bold"},
                    page_size=25,
                ),
                html.Hr(),
            ]
        )

    main_content = html.Div(
        [
            render_table(hitter_df, "Best Hitter Statistics", table_type="player"),
            render_table(pitcher_df, "Best Pitcher Statistics", table_type="player"),
            render_table(team_df, "Team Statistics"),
        ]
    )

    return sidebar, main_content


def register_callbacks(app):
    # Populate league dropdown on load
    @app.callback(
        Output("league-dropdown", "options"),
        Input("league-dropdown", "id")  # dummy input to trigger on load
    )
    def populate_league_options(_):
        leagues = sorted(data["team"]["league"].dropna().unique())
        return [{"label": league, "value": league} for league in leagues]

    # Populate year dropdown based on selected league
    @app.callback(
        Output("year-dropdown", "options"),
        Input("league-dropdown", "value")
    )
    def update_year_options(selected_league):
        if not selected_league:
            return []
        years = data["team"][data["team"]["league"] == selected_league]["year"].dropna().unique()
        return [{"label": str(year), "value": str(year)} for year in sorted(years)]

    # Update dashboard based on league and year
    @app.callback(
        Output("intro-block", "children"),
        Output("dynamic-content", "children"),
        Input("league-dropdown", "value"),
        Input("year-dropdown", "value")
    )
    def dashboard_callback(league, year):
        return update_dashboard(league, year)
