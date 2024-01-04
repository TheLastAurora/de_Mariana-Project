import dash_bootstrap_components as dbc
from dash import html, dcc


def create_card(header: int, subtitle: str, message: str) -> dbc.Card:
    if header:
        return dbc.Card(
            dbc.CardBody(
                [
                    html.H3(f"{header}th", style={"font-weight": "bold"}),
                    html.H4(subtitle),
                    dcc.Markdown(message),
                ],
            ),
            className="info-card text-center",
        )
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(
                    "No information avaliable for this Country.",
                    style={"font-weight": "bold"},
                ),
            ],
        ),
        className="info-card text-center",
    )
