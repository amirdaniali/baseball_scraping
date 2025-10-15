from dash import Dash
from visualisation.data_loader import load_all_data, get_league_year_options
from visualisation.layout import build_layout
from visualisation.callbacks import register_callbacks

data = load_all_data()
options = get_league_year_options(data["hitter"])

app = Dash(__name__)
app.layout = build_layout(options)
register_callbacks(app)
