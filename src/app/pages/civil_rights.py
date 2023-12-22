import dash
from dash import dcc, callback
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
import polars as pl
import plotly.express as px
import taxes
import sys

tax_per_country_df = taxes.tax_per_country()

layout = dbc.Container(
    [
        html.H2(id="selected-country", style={"font-weight": "bold"}),
        dcc.Dropdown(
            options=[
                {"label": country, "value": country}
                for country in tax_per_country_df["name"].unique().sort()
            ],
            placeholder="Select a Country",
            value="Brazil",
            id="dropdown-countries",
        ),
        html.Div(
            [
                html.H3("Tax progression over years"),
                dcc.Graph(id="taxes-year-graph"),
            ]
        ),
        html.Div(),
    ],
    id="civil-rights-container",
)


@callback(Output("selected-country", "children"), Input("dropdown-countries", "value"))
def get_selected_country(value):
    return value


@callback(
    Output("taxes-year-graph", "figure"),
    Input("dropdown-countries", "value"),
)
def update_taxes_country(country):
    df = tax_per_country_df.filter(pl.col("name") == country)
    fig = px.line(
        df,
        x="year",
        y=["mean_tariff_rate", "standard_deviation_of_tariff_rates", "tariffs"],
    )
    fig.update_layout(xaxis_title="Year", yaxis_title="Tariffs")
    fig.update_xaxes(tickvals=df["year"].unique(), tickmode="array")
    return fig
