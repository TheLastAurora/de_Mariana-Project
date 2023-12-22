import sys
import os

current_folder = os.path.dirname(os.path.abspath(__file__))
dags_path = os.path.join(current_folder, "..", "repository")
sys.path.insert(0, dags_path)

import database
import polars as pl


conn_wgi = database.DatabaseConnection("world-governance-index").connection
conn_ti = database.DatabaseConnection("transformation-index").connection
conn_ef = database.DatabaseConnection("economic-freedom").connection
conn_db = database.DatabaseConnection("doing-bussiness").connection


def property_rights() -> pl.DataFrame:
    wgi = pl.read_database(
        query="""
        SELECT name, year, estimate, rank
        FROM RuleOfLaw 
        LEFT JOIN iso_codes
        """,
        connection=conn_wgi
    )
