from dash import Input, Output, html, dcc
from components import layouts
from pages import home, error_404
from pages import state_governance
from pages import freedom
from components import layouts
import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
app.css.append_css({"external_url": "styles.css"})
app._favicon = "logo.png"


@app.callback(Output("page-content-container", "children"), Input("url", "pathname"))
def render_page(pathname: str) -> html.Div:
    # root
    if pathname == "/":
        return home.create_page(app)

    path = pathname.split("/")[1]
    # Freedom
    if path == "freedom":
        app.layout = layouts.layout(path)
        if pathname == "/freedom/civil_rights":
            return freedom.civil_rights.create_page(app)
        elif pathname == "/freedom/market-competition":
            return freedom.market_competition.create_page(app)
        elif pathname == "/freedom/tax-burden":
            return freedom.tax_burden.create_page(app)
        else:
            return error_404.create_page()

    # State Governance
    elif path == "state-governance":
        app.layout = layouts.layout(path)
        if pathname == "/state-governance/govern-effectiveness":
            return state_governance.govern_effectiveness.create_page(app)
        elif pathname == "/state-governance/economic-sustentability":
            return state_governance.economic_sustentability.create_page(app)
        elif pathname == "/state-governance/institutional-stability":
            return state_governance.institutional_stability.create_page(app)
        else:
            return error_404.create_page()
    # Errors
    else:
        return error_404.create_page()


if __name__ == "__main__":
    app.run(debug=True, dev_tools_hot_reload=True)
