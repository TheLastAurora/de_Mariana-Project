from re import M
import dash_bootstrap_components as dbc
from dash import html, dcc


def create_sidebar(path: str) -> html.Div:
    match path:
        case "freedom":
            return html.Div(
                [
                    html.H2([" Freedom"]),
                    html.Hr(),
                    html.P(
                        [
                            "“Each of us has a natural right, from God, to defend his person, his liberty, and his property.”",
                            html.Br(),
                            html.Br(),
                            dcc.Markdown("― *Frederic Bastiat*"),
                        ]
                    ),
                    html.Hr(),
                    dbc.Nav(
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
                    ),
                ],
                className="sidebar sidebar-freedom",
            )
        case "state-governance":
            return html.Div(
                [
                    html.H2(
                        [
                            "State",
                            html.Br(),
                            "Governance",
                        ],
                    ),
                    html.Hr(),
                    html.P(
                        [
                            "“When wicked or ignorant men govern, it is not surprising that virtue and goodness are not esteemed. For the former hate them, and the latter do not know them.”",
                            html.Br(),
                            html.Br(),
                            dcc.Markdown("― *Francesco Guicciardini*"),
                        ]
                    ),
                    html.Hr(),
                    dbc.Nav(
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
                    ),
                ],
                className="sidebar sidebar-state-governance",
            )
        case _:
            return html.Div(className="sidebar")
