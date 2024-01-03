import sys
import os
from math import floor
from typing import Tuple

current_folder = os.path.dirname(os.path.abspath(__file__))
dags_path = os.path.join(current_folder, "..", "repository")
sys.path.insert(0, dags_path)

import database
import polars as pl


conn_wgi = database.DatabaseConnection("world-governance-index").connection
conn_ti = database.DatabaseConnection("transformation-index").connection
conn_ef = database.DatabaseConnection("economic-freedom").connection
conn_db = database.DatabaseConnection("doing-bussiness").connection


def property_rights_ranking() -> pl.DataFrame:
    db_rank_registering_property = pl.read_database(
        query="""
        SELECT country_id, rank_registering_property
        FROM "freedom"
        WHERE YEAR = 2020
        ORDER BY rank_registering_property
        """,
        connection=conn_db,
    )

    ef_property_rights = pl.read_database(
        query="""
            SELECT country_id, real_property, property_rights
            FROM "freedom"
            WHERE YEAR = 2020
            ORDER BY country_id
            """,
        connection=conn_ef,
    )

    ti_property_rights = pl.read_database(
        query="""
            SELECT country_id, property_rights, private_property
            FROM "freedom"
            WHERE YEAR = 2020
            ORDER BY country_id
            """,
        connection=conn_ti,
    )

    ef_weights = [1.5, 1.0]
    ti_weights = [0.5, 0.5]
    db_weight = 3.5
    ef_property_rights = ef_property_rights.with_columns(
        pl.fold(
            acc=pl.lit(0),
            function=lambda c1, c2: c1 + c2,
            exprs=[
                pl.col(col) * pl.lit(wgt)
                for col, wgt in zip(ef_property_rights.columns[1:], ef_weights)
            ],
        ).alias("score")
    ).sort(by="score", descending=True)

    ef_property_rights = ef_property_rights.with_columns(
        ef_rank=ef_property_rights["score"].rank("ordinal", descending=True)
    ).select(pl.col(["country_id", "ef_rank"]))

    ti_property_rights = ti_property_rights.with_columns(
        pl.sum_horizontal(pl.exclude("country_id")).rank("ordinal").alias("ti_rank")
    ).select(pl.col(["country_id", "ti_rank"]))

    db_rank_registering_property = db_rank_registering_property.rename(
        {"rank_registering_property": "db_rank"}
    )

    df = db_rank_registering_property.join(
        ef_property_rights, how="left", on="country_id"
    ).join(ti_property_rights, how="left", on="country_id")

    return df.sort(
        by=["ef_rank", "db_rank", "ti_rank"], descending=False, nulls_last=True
    )
