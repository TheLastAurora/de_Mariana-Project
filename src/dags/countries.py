import polars as pl
import dash_bootstrap_components as dbc
import database

db = database.DatabaseConnection("economic-freedom").connection


def countries_per_region() -> pl.DataFrame:
    countries = pl.read_database(
        """SELECT name, "alpha-3", region from iso_codes""", connection=db
    )
    return (
        countries.group_by("region")
        .agg(pl.col("name"))
        .drop_nulls()
        .sort(pl.col("region"))
    )


def country_group() -> list:
    COUNTRIES = countries_per_region()
    country_group = []
    i = 0
    for sr, cs in COUNTRIES.iter_rows():
        country_group.append(
            dbc.ListGroupItem(sr.upper(), style={"font-weight": "900"})
        )
        for c in cs:
            country_group.append(
                dbc.ListGroupItem(
                    c,
                    action=True,
                    active=False,
                    style={"font-weight": "light", "cursor": "pointer"},
                    id={"type": "list-group-item", "index": i},
                    n_clicks=0,
                )
            )
            i += 1
    return country_group
