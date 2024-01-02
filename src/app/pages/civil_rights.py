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
        # html.H2(id="selected-country", style={"font-weight": "bold"}),
        html.Div(
            [
                html.H4("Tax progression over years"),
                dcc.Graph(id="taxes-year-graph"),
            ]
        ),
        html.Div(),
    ],
    id="civil-rights-container",
)


@callback(
    Output("taxes-year-graph", "figure"),
    Input("selected-country", "value"),
)
def update_taxes_country(country: str):
    df = tax_per_country_df.filter(pl.col("name") == country)
    fig = px.line(
        df,
        x="year",
        y=["mean_tariff_rate", "standard_deviation_of_tariff_rates", "tariffs"],
    )
    fig.update_layout(xaxis_title="Year", yaxis_title="Tariffs")    
    fig.update_xaxes(tickvals=df["year"].unique(), tickmode="array")
    return fig
