from dash import html, dcc


def build_layout(data, default_league, default_year):
    league_options = [
        {"label": league, "value": league}
        for league in sorted(data["team"]["league"].dropna().unique())
    ]
    year_options = [
        {"label": str(year), "value": str(year)}
        for year in sorted(data["team"][data["team"]["league"] == default_league]["year"].dropna().unique())
    ]

    return html.Div(
        style={
            "display": "flex",
            "flexDirection": "row",
            "gap": "2rem",
            "padding": "2rem",
            "fontFamily": "Segoe UI, sans-serif",
            "backgroundColor": "#f9f9f9",
            "color": "#000000",
        },
        children=[
            # Sidebar
            html.Div(
                style={
                    "flex": "1",
                    "maxWidth": "30%",
                    "backgroundColor": "#ffffff",
                    "padding": "1.5rem",
                    "borderRadius": "10px",
                    "boxShadow": "0 4px 12px rgba(0,0,0,0.05)",
                    "overflowY": "auto",
                    "maxHeight": "90vh",
                },
                children=[
                    html.H1("Baseball Stats Dashboard", style={"fontSize": "1.8rem"}),
                    html.P("Explore historical baseball data by league and year."),
                    html.Div([
                        html.Div([
                            html.Label("Select League"),
                            dcc.Dropdown(
                                id="league-dropdown",
                                options=league_options,
                                value=default_league,
                                placeholder="Choose a league",
                            ),
                        ]),
                        html.Div([
                            html.Label("Select Year"),
                            dcc.Dropdown(
                                id="year-dropdown",
                                options=year_options,
                                value=default_year,
                                placeholder="Choose a year",
                                searchable=True,
                            ),
                        ]),
                        html.Hr(),
                        html.Div(id="intro-block"),
                    ]),
                ],
            ),
            # Main content
            html.Div(
                id="main-content",
                style={
                    "flex": "2",
                    "maxWidth": "65%",
                    "backgroundColor": "#ffffff",
                    "padding": "1.5rem",
                    "borderRadius": "10px",
                    "boxShadow": "0 4px 12px rgba(0,0,0,0.05)",
                    "minHeight": "400px",
                },
                children=[
                    html.H2("Data & Visualizations", style={"marginBottom": "1rem"}),
                    html.Div(id="dynamic-content"),
                ],
            ),
        ],
    )
