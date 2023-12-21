import dash
from dash import dcc, callback
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
import polars as pl


layout = html.Div([dcc.Graph()])


# @callback(Input(["countries", "value"]), Output(["taxes-country-graph", "figure"]))
# def update_taxes_country():