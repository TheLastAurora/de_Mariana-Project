from dash import dcc, callback
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
import polars as pl
import plotly.express as px
import taxes

tax_per_country_df = taxes.tax_per_country()

layout = dbc.Container(
    [
        html.H2(id="selected-country", style={"font-weight": "bold"}),
        html.Div(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3("34th", style={"font-weight": "bold"}),
                            html.H4("WGI Overral Index"),
                            html.P("Among the worst 46%"),
                        ],
                    ),
                    className="info-card text-center",
                ),
            ],
            className="cards-div",
            style={"display": "flex", "flex-direction": "row"},
        ),
    ],
    id="civil-rights-container",
)


@callback(
    Output("taxes-year-graph", "figure"),
    Input("selected-country", "value"),
)
def update_taxes_country(country_id: int):
    df = tax_per_country_df.filter(pl.col("country_id") == country_id)
    fig = px.line(
        df,
        x="year",
        y=["mean_tariff_rate", "standard_deviation_of_tariff_rates", "tariffs"],
    )
    fig.update_layout(xaxis_title="Year", yaxis_title="Tariffs")
    fig.update_xaxes(tickvals=df["year"].unique(), tickmode="array")
    return fig


# @callback()
# def test():
#     pass
