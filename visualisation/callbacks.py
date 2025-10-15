from dash import Input, Output, html, dash_table
from visualisation.data_loader import load_all_data

data = load_all_data()


def update_dashboard(league_year):
    if not league_year or "|" not in league_year:
        return html.Div("Please select a league and year."), html.Div(
            "No data available."
        )

    league, year = league_year.split("|")
    league, year = league_year.split("|")
    intro = data["intro"]
    meta = data["meta"]
    hitter = data["hitter"]
    team = data["team"]

    # Sidebar content (unchanged)
    intro_texts = intro[(intro["league"] == league) & (intro["year"] == year)]
    h1_rows = intro_texts[intro_texts["type"] == "h1"]
    h2_rows = intro_texts[intro_texts["type"] == "h2"]

    sidebar = []
    for _, row in h1_rows.iterrows():
        sidebar.append(html.H2(row["title"]))
    grouped = h2_rows.groupby("title")
    for section_title, group in grouped:
        sidebar.append(html.H3(section_title))
        for _, row in group.iterrows():
            sidebar.append(html.P(row["paragraph"]))

    # Filtered tables
    meta_df = meta[(meta["league"] == league) & (meta["year"] == year)]
    hitter_df = hitter[(hitter["league"] == league) & (hitter["year"] == year)]
    team_df = team[(team["league"] == league) & (team["year"] == year)]

    def render_table(df, title):
        if df.empty:
            return html.Div(f"No data available for {title}.")
        return html.Div(
            [
                html.H4(title),
                dash_table.DataTable(
                    columns=[{"name": col, "id": col} for col in df.columns],
                    data=df.to_dict("records"),
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left", "padding": "5px"},
                    style_header={"backgroundColor": "#f0f0f0", "fontWeight": "bold"},
                    page_size=10,
                ),
                html.Hr(),
            ]
        )

    quote_text = meta_df["quote"].dropna().values
    quote_block = html.Div(
        [
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
            html.Hr(),
        ]
    )
    main_content = html.Div(
        [
            quote_block,
            render_table(hitter_df, "Player Statistics"),
            render_table(team_df, "Team Statistics"),
        ]
    )

    return sidebar, main_content


def register_callbacks(app):
    app.callback(
        Output("intro-block", "children"),
        Output("dynamic-content", "children"),
        Input("league-year", "value"),
    )(update_dashboard)
