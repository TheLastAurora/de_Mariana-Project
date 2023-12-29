import polars as pl
import dash_bootstrap_components as dbc


def countries_per_region() -> pl.DataFrame:
    countries = pl.read_csv("src/repository/DUMP/ISO CODE.csv")
    countries = countries.select(pl.col(["name", "alpha-3", "region"]))
    return (
        countries.group_by("region")
        .agg(pl.col("name"))
        .drop_nulls()
        .sort(pl.col("region"))
    )


def country_group() -> list:
    COUNTRIES = countries_per_region()
    country_group = []
    for sr, cs in COUNTRIES.iter_rows():
        country_group.append(
            dbc.ListGroupItem(sr.upper(), style={"font-weight": "900"})
        )
        for c in cs:
            country_group.append(
                dbc.ListGroupItem(
                    c,
                    style={"font-weight": "light"},
                    action=True,
                    id={"type": "list-group-item", "index": c}
                )
            )
    # I'm ignoring Antartica for AESTHETIC reasons in the sidebar.
    return country_group[2:]
