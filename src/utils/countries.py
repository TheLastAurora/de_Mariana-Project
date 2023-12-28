import polars as pl
import os

def countries_per_region() -> pl.DataFrame:
    countries = pl.read_csv("src/repository/DUMP/ISO CODE.csv")
    countries = countries.select(pl.col(["name", "alpha-3", "region"]))
    return countries.group_by("region").agg(pl.col("name")).drop_nulls().sort(pl.col("region"))
