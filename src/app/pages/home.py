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
                    "Freedom is appraised through civil and political rights, market dynamics, and societal traditions. Civil liberties, market competition, and protection of property rights and private enterprise are integral considerations. The evaluation also encompasses gender disparities, the legal system's role in shaping freedom, and ease of doing business. Assessments of monetary and fiscal policies, trade regulations, labor market dynamics, and World Governance Indicators contribute to a holistic understanding of a nation's freedom landscape.",
                    className="text-start font-italic",
                ),
                html.A(
                    html.H2("FREEDOM", className="font-weight-bold"),
                    href="/freedom",
                    id="freedom-link",
                ),
            ],
            className="d-flex align-items-center flex-col text-justify home-half",
            id="freedom-home",
        ),
        html.Div(
            [
                html.A(
                    html.H2("STATE GOVERNANCE"), href="/state-governance", id="sg-link"
                ),
                html.P(
                    "State Governance involves a comprehensive evaluation of a nation's political and administrative landscape, covering democratic institutions, socioeconomic development, and effective policy implementation. The Transformation Index assesses the health of democratic processes, commitment to democratic values, and socioeconomic barriers. It also scrutinizes challenges such as conflict intensity and evaluates governance effectiveness. Economic stability, welfare policies, and consensus-building contribute to the overall governance framework.",
                    className="text-end font-italic",
                ),
            ],
            className="d-flex align-items-center flex-col text-justify home-half",
            id="sg-home",
        ),
    ],
    id="home-container",
    className="d-flex flex-row h-100 w-100",
)
