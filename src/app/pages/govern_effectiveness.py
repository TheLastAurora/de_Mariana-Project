import dash
from dash import dcc, callback
from typing import Tuple
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
import polars as pl
import database
import polars as pl


db = database.DatabaseConnection("economic-freedom").connection


df = pl.read_database(query="SELECT * FROM freedom", connection=db)
iso_codes = pl.read_database(query="SELECT * FROM iso_codes", connection=db)


df.join(iso_codes, left_on="country_id", right_on="id", how="inner").select(
    pl.exclude(iso_codes.columns), pl.col("name")
).sort(pl.col(["year"]), descending=False).filter(pl.col("name") == "Brazil")


layout = html.Div(
    [],
)


@callback([Output("gov-effec-graph", "children"), Input("countries", "value")])
def update_tax_contries() -> html.Div:
    df = ""
    return html.Div([dcc.Dropdown(), dcc.Graph()])
