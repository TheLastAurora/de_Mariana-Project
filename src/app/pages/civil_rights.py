from dash import dcc, callback
import dash_bootstrap_components as dbc
from dash import html
from math import floor
from dash.dependencies import Input, Output, State
import polars as pl
import plotly.express as px

# Dags importing
import taxes
import civil_rights

tax_per_country_df = taxes.tax_per_country()
property_rights_df = civil_rights.property_rights_ranking()

layout = dbc.Container(
    [
        html.H2(id="selected-country", style={"font-weight": "bold"}),
        html.Div(
            [dbc.Card(id="property-rights-card")],
            className="cards-div",
            style={"display": "flex", "flex-direction": "row"},
        ),
    ],
    id="civil-rights-container",
)


@callback(
    Output("property-rights-card", "children"), Input("selected-country", "value")
)
def property_rights(country_id: str) -> dbc.Card:
    """Extracting for the specific country"""
    df = property_rights_df
    try:
        ranking = df.select(pl.arg_where(pl.col("country_id") == country_id)).item()
        status = "best" if ranking <= floor(len(df) / 2) else "worst"
        percentage = (
            ranking / len(df) * 100
            if status is "best"
            else 100 - ranking / len(df) * 100
        )
        comparison = (
            "Among the **{:.1f}% {}** countries in safeguarding this right.".format(
                percentage, status
            )
        )
        return dbc.Card(
            dbc.CardBody(
                [
                    html.H3(f"{ranking}th", style={"font-weight": "bold"}),
                    html.H4("Property Rights Index"),
                    dcc.Markdown(comparison),
                ],
            ),
            className="info-card text-center",
        )

    except ValueError:
        return dbc.Card(
            dbc.CardBody(
                [
                    html.H4(
                        "No information on Property Rights avaliable for this Country.",
                        style={"font-weight": "bold"},
                    ),
                ],
            ),
            className="info-card text-center",
        )


def freedom_of_labour_right():
    pass


def freedom_of_expression_right():
    pass
