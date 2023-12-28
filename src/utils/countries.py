import polars as pl
import os

print(os.getcwd())

def get_countries() -> pl.DataFrame:
    countries = pl.read_csv("src/repository/DUMP/ISO CODE.csv")
    return countries.select(pl.col(["name", "alpha-3", "region"]))
