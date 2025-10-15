from dash import html, dcc


def build_layout(options):
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
                    dcc.Dropdown(
                        id="league-year",
                        options=options,
                        value=options[0]["value"],
                        style={"marginBottom": "1.5rem"},
                    ),
                    html.Div(id="intro-block"),
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
                    "overflowX": "auto",  # enables horizontal scroll
                },
                children=[
                    html.H2("Data & Visualizations", style={"marginBottom": "1rem"}),
                    html.Div(id="dynamic-content"),
                ],
            ),
        ],
    )
