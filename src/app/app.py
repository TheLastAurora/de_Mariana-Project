import os
import sys

current_folder = os.path.dirname(os.path.abspath(__file__))
dags_path = os.path.join(current_folder, "..", "dags")
sys.path.insert(0, dags_path)


from typing import Tuple
from dash import Input, Output, html, dcc
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
from components.sidebar import create_sidebar
import dash_bootstrap_components as dbc
import dash


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
    ],
    id="full-page",
)
app.css.append_css({"external_url": "styles.css"})
app.title = "de Mariana"
app._favicon = "logo.png"


@app.callback(
    [Output("page-content", "children"), Output("sidebar", "children")],
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


if __name__ == "__main__":
    app.run(debug=True, dev_tools_hot_reload=True)
