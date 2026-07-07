"""
Pulls aggregated daily sales from fct_daily_sales for time-series forecasting.
"""

import os
import pymssql
import pandas as pd

DB_CONFIG = {
    "server": "retaildemandsqlserverus.database.windows.net",
    "user": "kingsleyadmin",
    "password": os.environ["DB_PASSWORD"],
    "database": "retaildemanddbus",
}

DAILY_SALES_QUERY = """
    SELECT
        sale_date,
        SUM(total_units_sold) AS total_units_sold
    FROM dbo.fct_daily_sales
    GROUP BY sale_date
    ORDER BY sale_date
"""


def get_daily_sales() -> pd.DataFrame:
    """Return total units sold per day, aggregated across all stores and items."""
    with pymssql.connect(**DB_CONFIG) as conn:
        return pd.read_sql(DAILY_SALES_QUERY, conn)


def main():
    df = get_daily_sales()
    print(f"Pulled {len(df):,} daily records")
    print(f"Date range: {df['sale_date'].min()} to {df['sale_date'].max()}")
    print(df.head())


if __name__ == "__main__":
    main()
