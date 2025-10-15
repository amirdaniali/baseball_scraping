## Amir Daniali
## Code the Dream
## Final Webscraping Project
## Week 14
## Final Part: Data Visualisation

from dash import Dash
from visualisation.data_loader import load_all_data
from visualisation.layout import build_layout
from visualisation.callbacks import register_callbacks

# Load all data once at startup
data = load_all_data()

# Set default league and year
DEFAULT_LEAGUE = "National League"
DEFAULT_YEAR = "2025"

app = Dash(__name__)
server = app.server
app.layout = build_layout(data, DEFAULT_LEAGUE, DEFAULT_YEAR)
register_callbacks(app, data)
