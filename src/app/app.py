import dash
import dash_bootstrap_components as dbc
from components import layout


def main() -> None:
    app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "de Mariana"
    app._favicon = "logo.png"
    app.layout = layout.create_layout(app)
    app.run(debug=True)


if __name__ == "__main__":
    main()
