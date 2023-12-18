import dash
from app import app
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State


dash.register_page(
    __name__,
    title="Civil Right index",
    description="The Civil Right page shows statitical reports on how recognized are the basic human rights .",
)


def create_page(app: dash.Dash) -> html.Div:
    @app.callback(Output="")
    def get_page():
        return html.Div()

    return get_page()
