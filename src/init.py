from repository import database
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import polars as pl

conn = database.DatabaseConnection(db_name="economic-freedom").connection

df = pl.read_database(query="SELECT * FROM freedom", connection=conn)
iso_codes = pl.read_database(query="SELECT * FROM iso_codes", connection=conn)

app = Dash(__name__)

countries = (
    df.join(iso_codes, left_on="country_id", right_on="id", how="inner")
    .select(pl.exclude(iso_codes.columns), pl.col("name"))
    .unique()
)


dropdown_options = [
    {"label": country, "value": country}
    for country in countries.get_column("name").to_list()
]

app.layout = html.Div(
    [
        html.H1(children="Tax Compliance", style={"textAlign": "center"}),
        dcc.Dropdown(options=dropdown_options, value="Brazil", id="dropdown-selection"),
        dcc.Graph(id="graph-content"),
    ]
)


@app.callback(Output("graph-content", "figure"), [Input("dropdown-selection", "value")])
def update_graph(value):
    dff = countries.sort(pl.col(["name", "year"])).filter(pl.col("name") == value)
    fig = px.line(dff, x="year", y="impartial_public_administration")
    fig.update_layout(xaxis_tickformat="d")
    return fig


if __name__ == "__main__":
    app.run(debug=True)
