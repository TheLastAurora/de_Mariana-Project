import database
import polars as pl


db = database.DatabaseConnection("economic-freedom").connection


def tax_per_country() -> pl.DataFrame:
    df = pl.read_database(
        query="""
        SELECT year, country_id, top_marginal_income_tax_rate, top_marginal_income_and_payroll_tax_rate, top_marginal_tax_rate, trade_tax_revenue, mean_tariff_rate, standard_deviation_of_tariff_rates, tariffs 
        FROM freedom;
            """,
        connection=db,
    )
    iso_codes = pl.read_database(query="SELECT * FROM iso_codes", connection=db)
    return (
        df.join(iso_codes, left_on="country_id", right_on="id", how="inner")
        .select(pl.exclude(iso_codes.columns), pl.col("name"))
        .sort(pl.col(["year"]), descending=False)
    )
