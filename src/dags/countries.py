import polars as pl
import dash_bootstrap_components as dbc
import database

db = database.DatabaseConnection("economic-freedom").connection


def countries_per_region() -> pl.DataFrame:
    countries = pl.read_database(
        """SELECT id, name, "alpha-3", region from iso_codes""", connection=db
    )
    return (
        countries.group_by("region")
        .agg(pl.col("id"))
        .drop_nulls()  # This removes Antartica. Remove as you wish.
        .sort(pl.col("region"))
    )


def country_by_id(id: int) -> str:
    country = pl.read_database(
        f"SELECT name FROM iso_codes WHERE id = {id}", connection=db
    ).item()
    return country


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
                    children=country_by_id(c),  # Country name
                    key=c,  # Country id
                    id={"type": "list-group-item", "index": i},
                    action=True,
                    active=False,
                    style={"font-weight": "light", "cursor": "pointer"},
                    n_clicks=0,
                )
            )
            i += 1
    return country_group
