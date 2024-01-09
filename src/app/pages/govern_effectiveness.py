import dash
from dash import dcc, callback
from typing import Tuple
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output

layout = html.Div(
    [
        html.H2("Maintenance"),
        html.Img(src="/assets/maintenance.png", width="150px", height="150px"),
    ],
    className="d-flex flex-column justify-content-center align-items-center w-100",
)
