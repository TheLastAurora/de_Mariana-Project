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
        WHERE "year" = 2020
        ORDER BY rank_registering_property
        """,
        connection=conn_db,
    )

    ef_property_rights = pl.read_database(
        query="""
            SELECT country_id, real_property, property_rights
            FROM "freedom"
            WHERE "year" = 2020
            ORDER BY country_id
            """,
        connection=conn_ef,
    )

    ti_property_rights = pl.read_database(
        query="""
            SELECT country_id, property_rights, private_property
            FROM "freedom"
            WHERE "year" = 2020
            ORDER BY country_id
            """,
        connection=conn_ti,
    )

    ef_weights = [1.5, 1.0]
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


def freedom_of_labour_ranking() -> pl.DataFrame:
    db_labour = pl.read_database(
        query="""
    SELECT country_id, labor_tax_and_contributions 
    FROM "freedom" 
    WHERE "year" = 2020 
    ORDER BY country_id
    """,
        connection=conn_db,
    )

    ef_labour = pl.read_database(
        query="""
        SELECT country_id, labor_regulations_and_minimum_wage, hiring_and_firing_regulations, flexible_wage_determination, hours_regulations, cost_of_worker_dismissal, foreign_labor, labor_market_regulations 
        FROM "freedom" 
        WHERE "year" = 2020 
        ORDER BY country_id
        """,
        connection=conn_ef,
    )

    ti_labour = pl.read_database(
        query="""
        SELECT country_id, private_enterprise 
        FROM "freedom" 
        WHERE "year" = 2020 
        ORDER BY country_id
        """,
        connection=conn_ti,
    )

    wgi_labour_rank = pl.read_database(
        query="""
        SELECT country_id, rank 
        FROM "VoiceAccountability" 
        WHERE "year" = 2020
        ORDER BY country_id
        """,
        connection=conn_wgi,
    )

    ef_weights = {
        "labor_regulations_and_minimum_wage": 2,
        "hiring_and_firing_regulations": 2,
        "flexible_wage_determination": 3,
        "hours_regulations": 3,
        "cost_of_worker_dismissal": 1.5,
        "foreign_labor": 1,
        "labor_market_regulations": 1.5,
    }

    ef_labour = ef_labour.with_columns(
        pl.fold(
            acc=pl.lit(0),
            function=lambda c1, c2: c1 + c2,
            exprs=[pl.col(col) * pl.lit(wgt) for col, wgt in ef_weights.items()],
        ).alias("score")
    ).sort(by="score", descending=True)

    ef_rank = ef_labour.with_columns(
        ef_rank=ef_labour["score"].rank("ordinal", descending=True)
    ).select(pl.col(["country_id", "ef_rank"]))

    db_labour = db_labour.sort(by="labor_tax_and_contributions", descending=True)
    db_rank = db_labour.with_columns(
        db_rank=db_labour["labor_tax_and_contributions"].rank(
            "ordinal", descending=True
        )
    ).select(pl.exclude("labor_tax_and_contributions"))

    ti_labour = ti_labour.sort(by="private_enterprise", descending=True)
    ti_rank = ti_labour.with_columns(
        ti_rank=ti_labour["private_enterprise"].rank("ordinal", descending=True)
    ).select(pl.exclude("private_enterprise"))

    wgi_rank = wgi_labour_rank.rename({"rank": "wgi_rank"})

    df = (
        wgi_rank.join(ef_rank, on="country_id", how="left")
        .join(ti_rank, on="country_id", how="left")
        .join(db_rank, on="country_id", how="left")
    )

    return df.sort(by=["ef_rank", "ti_rank", "db_rank", "wgi_rank"], nulls_last=True)


def freedom_of_expression_ranking() -> pl.DataFrame:
    ef_expression = pl.read_database(
        query="""
    SELECT country_id, freedom_of_foreigners_to_visit 
    FROM "freedom" 
    WHERE "year" = 2020 
    ORDER BY country_id
    """,
        connection=conn_ef,
    )

    ti_expression = pl.read_database(
        query="""
        SELECT country_id, freedom_of_expression 
        FROM "freedom" 
        WHERE "year" = 2020 
        ORDER BY country_id
        """,
        connection=conn_ti,
    )

    wgi_expression_rank = pl.read_database(
        query="""
        SELECT country_id, rank 
        FROM "VoiceAccountability" 
        WHERE "year" = 2020
        ORDER BY country_id
        """,
        connection=conn_wgi,
    )
    ef_expression = ef_expression.sort(
        by="freedom_of_foreigners_to_visit", descending=True
    )
    ef_rank = ef_expression.with_columns(
        ef_rank=ef_expression["freedom_of_foreigners_to_visit"].rank(
            "ordinal", descending=True
        )
    ).select(pl.exclude("freedom_of_foreigners_to_visit"))

    ti_expression = ti_expression.sort(by="freedom_of_expression", descending=True)
    ti_rank = ti_expression.with_columns(
        ti_rank=ti_expression["freedom_of_expression"].rank("ordinal", descending=True)
    ).select(pl.exclude("freedom_of_expression"))

    wgi_rank = wgi_expression_rank.rename({"rank": "wgi_rank"})

    df = wgi_rank.join(ef_rank, on="country_id", how="left").join(
        ti_rank, on="country_id", how="left"
    )

    return df.sort(by=["ti_rank", "ef_rank", "wgi_rank"], nulls_last=True)
