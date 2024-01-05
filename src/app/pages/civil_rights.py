from typing import Tuple
from dash import dcc, callback
import dash_bootstrap_components as dbc
from dash import html
from math import floor
from dash.dependencies import Input, Output, State
from components.index_card import create_card
import polars as pl
import plotly.graph_objects as go
import plotly.express as px

# Dags importing
import taxes
import civil_rights
from countries import country_by_id

tax_per_country_df = taxes.tax_per_country()

# Cards
property_rights_df = civil_rights.property_rights_ranking()
freedom_of_labour_right_df = civil_rights.freedom_of_labour_ranking()
freedom_of_expression_right_df = civil_rights.freedom_of_expression_ranking()
religious_freedom_df = civil_rights.religious_freedom_score()

# Graphs
cr_per_country_year_df = civil_rights.cr_per_country_year()

layout = dbc.Container(
    [
        html.H2(
            id="selected-country",
            style={"font-weight": "bold", "margin-bottom": "1em"},
        ),
        html.Div(
            [
                dbc.Card(id="property-rights-card", className="info-card text-center"),
                dbc.Card(id="freedom-labour-card", className="info-card text-center"),
                dbc.Card(
                    id="freedom-expression-card", className="info-card text-center"
                ),
            ],
            className="cards-div",
            style={"display": "flex", "flex-direction": "row", "gap": "1rem"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="civil-rights-evolution-graph"),
                        dcc.Markdown(
                            id="civil-rights-evolution-report", className="text-center"
                        ),
                    ],
                ),
                html.Div(
                    dbc.Card(
                        id="religious-freedom-card", className="info-card text-center"
                    )
                ),
            ],
            className="d-flex flex-row",
        ),
    ],
    id="civil-rights-container",
)


@callback(
    Output("property-rights-card", "children"), Input("selected-country", "value")
)
def property_rights(country_id: int) -> dbc.Card:
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
def freedom_of_labour_right(country_id: int) -> dbc.Card:
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
def freedom_of_expression_right(country_id: int) -> dbc.CardBody:
    df = freedom_of_expression_right_df
    try:
        ranking = df.select(pl.arg_where(pl.col("country_id") == country_id)).item()
        status = "best" if ranking <= floor(len(df) / 2) else "worst"
        percentage = (
            ranking / len(df) * 100
            if status == "best"
            else 100 - ranking / len(df) * 100
        )
        subtitle = "Freedom of Expression Index"
        message = "Among the **{:.1f}% {}** countries to express ideas.".format(
            percentage, status
        )
        return create_card(ranking, subtitle, message)
    except ValueError:
        return create_card(header=None)


@callback(
    [
        Output("civil-rights-evolution-graph", "figure"),
        Output("civil-rights-evolution-report", "children"),
    ],
    Input("selected-country", "value"),
)
def civil_rights_evolution(country_id: int) -> Tuple[go.Figure, str]:
    df = cr_per_country_year_df

    fig = go.Figure()
    world_tendency = (
        df.group_by(by="year").agg(pl.col("civil_rights").mean()).sort(by="year")
    )
    country_tendency = df.filter(pl.col("country_id") == country_id).sort(by="year")
    country_name = country_by_id(country_id)
    region_name = (
        df.filter(pl.col("country_id") == country_id).limit(1)["sub-region"].item()
    )
    region_tendency = (
        df.group_by(by=["year", "sub-region"])
        .agg(pl.col("civil_rights").mean())
        .filter(pl.col("sub-region") == region_name)
        .sort(by="year")
    )

    fig.add_trace(
        go.Scatter(
            x=world_tendency["year"],
            y=world_tendency["civil_rights"].round(1),
            name="World",
            mode="lines",
            connectgaps=True,
            line={"color": "black", "width": 3},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=region_tendency["year"],
            y=region_tendency["civil_rights"].round(1),
            name=region_name,
            mode="lines",
            connectgaps=True,
            line={"color": "orange", "width": 3},
        )
    )

    fig.add_trace(
        go.Scatter(
            x=country_tendency["year"],
            y=country_tendency["civil_rights"],
            mode="lines",
            name=country_name,
            connectgaps=True,
            line={"color": "red", "width": 3},
        )
    )

    fig.update_layout(
        title="<b>Civil Rights score</b>".upper(),
        xaxis=dict(title="Year"),
        yaxis=dict(
            title="Score",
            tickvals=list(range(11)),
        ),
    )
    percent = (
        country_tendency["civil_rights"][-1] - country_tendency["civil_rights"][0]
    ) / country_tendency["civil_rights"][-1]
    time_span = country_tendency["year"][-1] - country_tendency["year"][0]
    report = f"""The provided conditions for exercising Civil Rights in this country got overral {'**unchanged**'.upper() if percent == 0 else f'**{(abs(percent) * 100):.1f}% {"worst" if percent < 0 else "better"}**'.upper()} over the last {time_span} years."""
    return fig, report


@callback(
    Output("religious-freedom-card", "children"), Input("selected-country", "value")
)
def religious_freedom_status(country_id: int) -> dbc.Card():
    df = religious_freedom_df
    print(df)
