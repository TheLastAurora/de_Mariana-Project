from dash import Input, Output, dcc, html
from components import layout
from pages import home, error_404
from pages import state_governance
from pages import freedom
from components import layout
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app._favicon = "logo.png"


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page(pathname: str) -> html.Div:
    # root
    if pathname == "/":
        return home.create_page(app)

    # Freedom
    if pathname.split("/")[0] == "freedom":
        app.layout = layout.create_freedom_layout(app)
        if pathname == "/freedom/civil_rights":
            return freedom.civil_rights.create_page(app)
        elif pathname == "/freedom/market-competition":
            return freedom.market_competition.create_page(app)
        elif pathname == "/freedom/tax-burden":
            return freedom.tax_burden.create_page(app)
        else:
            return error_404.create_page()

    # State Governance
    elif pathname.split("/")[0] == "state-governance":
        app.layout = layout.create_state_governance_layout(app)
        if pathname == "state-governance/govern-effectiveness":
            return state_governance.govern_effectiveness.create_page(app)
        elif pathname == "state-governance/economic-sustentability":
            return state_governance.economic_sustentability.create_page(app)
        elif pathname == "state-governance/institutional-stability":
            return state_governance.institutional_stability.create_page(app)
        else:
            return error_404.create_page()
    # Errors
    else:
        return error_404.create_page()


if __name__ == "__main__":
    app.run(debug=True, dev_tools_hot_reload=True)
