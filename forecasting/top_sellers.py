"""
Identifies the top-selling store-item combinations by total units sold,
used to select which combinations get individual Prophet forecasts.
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

TOP_SELLERS_QUERY = """
    SELECT TOP 5
        store_id,
        item_id,
        SUM(total_units_sold) AS total_units_sold
    FROM dbo.fct_daily_sales
    GROUP BY store_id, item_id
    ORDER BY total_units_sold DESC
"""


def get_top_sellers() -> pd.DataFrame:
    with pymssql.connect(**DB_CONFIG) as conn:
        return pd.read_sql(TOP_SELLERS_QUERY, conn)


if __name__ == "__main__":
    df = get_top_sellers()
    print(df)
