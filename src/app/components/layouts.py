from dash import dcc
import dash_bootstrap_components as dbc
from dash import html


def layout(path: str) -> dbc.Container:
    layout = html.Div(
        [dcc.Location(id="url", refresh=False), html.Div(id="page-content-container")]
    )
    match path:
        case "freedom":
            sidebar = dbc.Nav(
                [
                    dbc.NavLink(
                        "Civil Rights",
                        href="/freedom/civil_rights",
                        active="exact",
                        className="sidebar-link",
                    ),
                    dbc.NavLink(
                        "Market Competition",
                        href="/freedom/market-competition",
                        active="exact",
                        className="sidebar-link",
                    ),
                    dbc.NavLink(
                        "Tax Burden",
                        href="/freedom/tax-burden",
                        active="exact",
                        className="sidebar-link",
                    ),
                ],
                vertical=True,
                pills=True,
                className="sidebar-freedom",
            )
            layout.children.append(
                dbc.Row(
                    [
                        dbc.Col(sidebar, width=3),
                        dbc.Col(
                            html.Div(id="page-content", className="content"), width=9
                        ),
                    ],
                    className="main-content",
                    fluid=True,
                )
            )

        case "state-governance":
            sidebar = dbc.Nav(
                [
                    dbc.NavLink(
                        "Govern Effectiveness",
                        href="/state-governance/govern-effectiveness",
                        active="exact",
                        className="sidebar-link",
                    ),
                    dbc.NavLink(
                        "Economic Sustainability",
                        href="/state-governance/economic-sustainability",
                        active="exact",
                        className="sidebar-link",
                    ),
                    dbc.NavLink(
                        "Institutional Stability",
                        href="/state-governance/institutional-stability",
                        active="exact",
                        className="sidebar-link",
                    ),
                ],
                vertical=True,
                pills=True,
                className="sidebar-state-governance",
            )

            layout.children.append(
                dbc.Row(
                    [
                        dbc.Col(sidebar, width=3),
                        dbc.Col(
                            html.Div(id="page-content", className="content"), width=9
                        ),
                    ],
                    className="main-content",
                    fluid=True,
                )
            )

        case _:
            layout.children = [html.H1("Failed to render Layout")]
    return layout
