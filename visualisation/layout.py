from dash import html, dcc


def build_layout(data, default_league, default_year):
    league_options = [
        {"label": league, "value": league}
        for league in sorted(data["team"]["league"].dropna().unique())
    ]
    year_options = [
        {"label": str(year), "value": str(year)}
        for year in sorted(
            data["team"][data["team"]["league"] == default_league]["year"]
            .dropna()
            .unique()
        )
    ]

    return html.Div(
        [
            html.Div(
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
                    build_sidebar(
                        league_options, year_options, default_league, default_year
                    ),
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
                            html.H2(
                                "Data & Visualizations",
                                id="main-title",
                                style={"textAlign": "center"},
                            ),
                            build_top_teams_section(),
                            build_historical_section(),
                            build_yearly_tables(),
                        ],
                    ),
                ],
            ),
            build_footer(),
        ]
    )


def build_yearly_tables():
    return html.Div(
        [
            html.Div(id="team-win-percentage-chart"),
            html.Div(id="team-statistics-table"),
            html.Div(id="hitter-statistics-table"),
            html.Div(id="pitcher-statistics-table"),
        ]
    )


def build_historical_section():
    return html.Div(
        [
            html.H3("Historical League Insights", id="historical-section-title"),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Select Role", htmlFor="role-select"),
                            dcc.Dropdown(
                                id="role-select",
                                options=[
                                    {"label": "Hitter", "value": "hitter"},
                                    {"label": "Pitcher", "value": "pitcher"},
                                ],
                                value="hitter",
                            ),
                        ],
                        style={"flex": "1", "marginRight": "1rem"},
                    ),
                    html.Div(
                        [
                            html.Label("Select Statistic", htmlFor="stat-select"),
                            dcc.Dropdown(
                                id="stat-select",
                                placeholder="Choose a statistic",
                                value="Hits",
                            ),
                        ],
                        style={"flex": "1"},
                    ),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "row",
                    "gap": "1rem",
                    "marginBottom": "1rem",
                },
            ),
            html.Div(id="historical-charts-container"),
        ],
        id="historical-section",
    )


def build_top_teams_section():
    return html.Div(
        [
            html.Div(id="top-teams-all-time-chart"),
        ],
        id="top-teams-section",
        style={"margin": "0 0", "textAlign": "center"},
    )


def build_sidebar(league_options, year_options, default_league, default_year):
    return html.Div(
        id="sidebar-container",
        style={
            "maxWidth": "30%",
            "padding": "1rem",
            "borderRadius": "10px",
        },
        children=[
            html.H1(
                "Baseball Stats Dashboard",
                id="sidebar-title",
                style={"fontSize": "1.8rem", "textAlign": "center"},
            ),
            html.P(
                "Explore historical baseball data by league and year.",
                id="sidebar-description",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Label("Select League", htmlFor="league-dropdown"),
                            dcc.Dropdown(
                                id="league-dropdown",
                                options=league_options,
                                value=default_league,
                                placeholder="Choose a league",
                            ),
                        ],
                        id="sidebar-league-selector",
                        style={"flex": "1", "marginRight": "1rem"},
                    ),
                    html.Div(
                        [
                            html.Label("Select Year", htmlFor="year-dropdown"),
                            dcc.Dropdown(
                                id="year-dropdown",
                                options=year_options,
                                value=default_year,
                                placeholder="Choose a year",
                                searchable=True,
                            ),
                        ],
                        id="sidebar-year-selector",
                        style={"flex": "1"},
                    ),
                ],
                id="sidebar-controls",
                style={
                    "display": "flex",
                    "flexDirection": "row",
                    "gap": "1rem",
                    "marginBottom": "1rem",
                },
            ),
            html.Hr(),
            html.Div(id="sidebar-intro-content"),
        ],
    )


def build_footer():
    return html.Footer(
        id="app-footer",
        style={
            "display": "flex",
            "flexDirection": "row",
            "gap": "1rem",
            "justifyContent": "center",
            "padding": "1rem",
            "fontSize": "0.9rem",
            "fontFamily": "Segoe UI, sans-serif",
            "backgroundColor": "#f9f9f9",
            "color": "#000000",
        },
        children=[
            html.Div("© Made by Amir Daniali."),
            html.A(
                "Github Link",
                href="https://github.com/amirdaniali/baseball_scraping",
                style={
                    "color": "#000000",
                },
                target="_blank",
            ),
        ],
    )
