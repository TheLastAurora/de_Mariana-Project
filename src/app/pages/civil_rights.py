from dash import dcc, callback
import dash_bootstrap_components as dbc
from dash import html
from math import floor
from dash.dependencies import Input, Output, State
from components.index_card import create_card
import polars as pl
import plotly.express as px

# Dags importing
import taxes
import civil_rights

tax_per_country_df = taxes.tax_per_country()

# Cards
property_rights_df = civil_rights.property_rights_ranking()
freedom_of_labour_right_df = civil_rights.freedom_of_labour_ranking()
freedom_of_expression_right_df = civil_rights.freedom_of_expression_ranking()

layout = dbc.Container(
    [
        html.H2(id="selected-country", style={"font-weight": "bold"}),
        html.Div(
            [
                dbc.Card(id="property-rights-card"),
                dbc.Card(id="freedom-labour-card"),
                dbc.Card(id="freedom-expression-card"),
            ],
            className="cards-div",
            style={"display": "flex", "flex-direction": "row", "gap": "1rem"},
        ),
    ],
    id="civil-rights-container",
)


@callback(
    Output("property-rights-card", "children"), Input("selected-country", "value")
)
def property_rights(country_id: str) -> dbc.Card:
    df = property_rights_df
    try:
        ranking = df.select(pl.arg_where(pl.col("country_id") == country_id)).item()
        status = "best" if ranking <= floor(len(df) / 2) else "worst"
        percentage = (
            ranking / len(df) * 100
            if status == "best"
            else 100 - ranking / len(df) * 100
        )
        subtitle = "Property Rights Index"
        message = "Among the **{:.1f}% {}** countries to have property.".format(
            percentage, status
        )
        return create_card(ranking, subtitle, message)
    except ValueError:
        return create_card(header=None)


@callback(Output("freedom-labour-card", "children"), Input("selected-country", "value"))
def freedom_of_labour_right(country_id: str) -> dbc.Card:
    df = freedom_of_labour_right_df
    try:
        ranking = df.select(pl.arg_where(pl.col("country_id") == country_id)).item()
        status = "best" if ranking <= floor(len(df) / 2) else "worst"
        percentage = (
            ranking / len(df) * 100
            if status == "best"
            else 100 - ranking / len(df) * 100
        )
        subtitle = "Freedom of Labour Index"
        message = "Among the **{:.1f}% {}** countries to work.".format(
            percentage, status
        )
        return create_card(ranking, subtitle, message)
    except ValueError:
        return create_card(header=None)


@callback(
    Output("freedom-expression-card", "children"), Input("selected-country", "value")
)
def freedom_of_expression_right(country_id: str) -> dbc.Card:
    df = freedom_of_expression_right_df
    try:
        ranking = df.select(pl.arg_where(pl.col("country_id") == country_id)).item()
        status = "best" if ranking <= floor(len(df) / 2) else "worst"
        percentage = (
            ranking / len(df) * 100
            if status == "best"
            else 100 - ranking / len(df) * 100
        )
        subtitle = "Freedom of Labour Index"
        message = "Among the **{:.1f}% {}** countries to express ideas.".format(
            percentage, status
        )
        return create_card(ranking, subtitle, message)
    except ValueError:
        return create_card(header=None)
