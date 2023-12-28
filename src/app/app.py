import os
import sys

current_folder = os.path.dirname(os.path.abspath(__file__))
dags_path = os.path.join(current_folder, "..", "dags")
utils_path = os.path.join(current_folder, "..", "utils")
sys.path.insert(0, dags_path)
sys.path.insert(0, utils_path)


from typing import Tuple
from dash import Input, Output, State, html, dcc
from pages import (
    home,
    civil_rights,
    market_competition,
    tax_burden,
    govern_effectiveness,
    economic_sustentability,
    institutional_stability,
    error_404,
)

from countries import countries_per_region
from components.sidebar import create_sidebar
import polars as pl
import dash_bootstrap_components as dbc
import dash

# Display the countries in the list
COUNTRIES = countries_per_region()
country_group = []
for sr, cs in COUNTRIES.iter_rows():
    country_group.append(dbc.ListGroupItem(sr.upper(), style={"font-weight": "900"}))
    for c in cs:
        country_group.append(dbc.ListGroupItem(c, style={"font-weight": "light"}, action=True))

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,
    suppress_callback_exceptions=True,
)
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Link(rel="stylesheet", href="/assets/style.css"),
        html.Div(id="sidebar"),
        html.Div(id="page-content", children=[]),
        html.Div(
            [
                dbc.Button(
                    [
                        html.Img(src="/assets/globe.png", id="globe"),
                        html.Img(src="/assets/globe_inverse.png", id="globe-inverse"),
                    ],
                    id="globe-button",
                    color="none",
                    n_clicks=0,
                ),
                dbc.Collapse(
                    [
                        dbc.ListGroup(country_group, flush=True),
                    ],
                    id="list-collapse",
                    is_open=False,
                ),
            ],
            id="globe-div",
        ),
    ],
    id="full-page",
)
app.css.append_css({"external_url": "styles.css"})
app.title = "de Mariana"
app._favicon = "logo.png"


@app.callback(
    [
        Output("page-content", "children"),
        Output("sidebar", "children"),
    ],
    [Input("url", "pathname")],
)
def render_page(pathname: str) -> Tuple[html.Div, html.Div]:
    section = pathname.split("/")[1]
    sidebar = create_sidebar(section)
    match pathname:
        case None:
            layout = home.layout
        case "/freedom/civil-rights":
            layout = civil_rights.layout
        case "/freedom/market-competition":
            layout = market_competition.layout
        case "/freedom/tax-burden":
            layout = tax_burden.layout

        case "/state-governance/govern-effectiveness":
            layout = govern_effectiveness.layout
        case "/state-governance/economic-sustainability":
            layout = economic_sustentability.layout
        case "/state-governance/institutional-stability":
            layout = institutional_stability.layout

        case _:
            layout = error_404.layout
    return layout, sidebar


@app.callback(
    Output("list-collapse", "is_open"),
    [Input("globe-button", "n_clicks")],
    [State("list-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run(debug=True, dev_tools_hot_reload=True)
