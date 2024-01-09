import dash_bootstrap_components as dbc
from dash import html, dcc


def create_card(header: int, subtitle: str, message: str) -> dbc.CardBody:
    if header:
        return dbc.CardBody(
            [
                html.H3(f"{header}th", style={"font-weight": "bold"}),
                html.H4(subtitle),
                dcc.Markdown(message),
            ],
        )

    return dbc.CardBody(
        [
            html.H4(
                "No information avaliable for this Country.",
                style={"font-weight": "bold"},
            ),
        ],
    )
