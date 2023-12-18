import dash
from app import app
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

def create_page(app: dash.Dash) -> html.Div:
    return html.Div()