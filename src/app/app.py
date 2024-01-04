import os
from pprint import pprint
import sys

current_folder = os.path.dirname(os.path.abspath(__file__))
dags_path = os.path.join(current_folder, "..", "dags")
utils_path = os.path.join(current_folder, "..", "utils")
repository_path = os.path.join(current_folder, "..", "repository")
sys.path.insert(0, repository_path)
sys.path.insert(0, dags_path)
sys.path.insert(0, utils_path)


from typing import Tuple
from dash import Dash, Input, Output, State, html, dcc, ctx, ALL
from dash_bootstrap_templates import load_figure_template
from dash.exceptions import PreventUpdate
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

from countries import country_group
from components.sidebar import create_sidebar
import polars as pl
import dash_bootstrap_components as dbc
import numpy as np


app = Dash(
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
                        html.H5("Select a Country", className="list-collapse-header"),
                        dbc.ListGroup(
                            country_group(), flush=True, id="sidebar-country-list"
                        ),
                    ],
                    id="list-collapse",
                    dimension="width",
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
load_figure_template("lux")

# Last selected country, or "Brazil", for default.
# This is not the country_id, but the index in list-group-item, instead.
LAST_SELECTED_COUNTRY = 71


@app.callback(
    [
        Output("page-content", "children"),
        Output("sidebar", "children"),
    ],
    [Input("url", "pathname")],
)
def render_page(pathname: str) -> Tuple[html.Div | dbc.Container, html.Div]:
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
def toggle_collapse(n, is_open) -> bool:
    if n:
        return not is_open
    return is_open


@app.callback(
    [
        Output("sidebar-country-list", "children"),
        Output("selected-country", "children"),
        Output("selected-country", "value"),
        Output("globe-button", "n_clicks"),
    ],
    [
        Input({"type": "list-group-item", "index": ALL}, "n_clicks"),
    ],
    State("sidebar-country-list", "children"),
)
def update_country(clicked, countries):
    global LAST_SELECTED_COUNTRY
    country_index = None
    try:
        country_index = np.nonzero(np.array(clicked))[0][0]
    except IndexError:
        country_index = LAST_SELECTED_COUNTRY
    LAST_SELECTED_COUNTRY = country_index
    country = None
    for c in countries:
        country_id = c.get("props").get("id")
        c.get("props")["active"] = False
        c.get("props")["n_clicks"] = 0
        if country_id and country_id["index"] == country_index:
            country = c

    country.get("props")["active"] = True
    return countries, country.get("props")["children"], country.get("props")["key"], 1


if __name__ == "__main__":
    app.run(debug=True, dev_tools_hot_reload=True)
