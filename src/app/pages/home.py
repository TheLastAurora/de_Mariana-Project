import dash
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output

layout = html.Div(
    [
        html.Div(
            [
                html.P(
                    "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
                ),
                html.A(html.H2("FREEDOM"), href="/freedom"),
            ],
            className="d-flex align-items-center flex-col text-justify home-half",
        ),
        html.Div(
            [
                html.A(html.H2("STATE GOVERNANCE"), href="/state-governance"),
                html.P(
                    "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
                ),
            ],
            className="d-flex align-items-center flex-col text-justify home-half",
        ),
    ],
    id="home-container",
    className="d-flex flex-row h-100 w-100",
)
""
