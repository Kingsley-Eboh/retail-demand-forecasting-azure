"""
Trains a Prophet model on daily retail sales and forecasts demand
90 days into the future.
"""

import os
import pymssql
import pandas as pd
from prophet import Prophet

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

FORECAST_HORIZON_DAYS = 90


def get_daily_sales() -> pd.DataFrame:
    """Return total units sold per day, aggregated across all stores and items."""
    with pymssql.connect(**DB_CONFIG) as conn:
        return pd.read_sql(DAILY_SALES_QUERY, conn)


def prepare_for_prophet(df: pd.DataFrame) -> pd.DataFrame:
    """Prophet requires exactly two columns: ds (date) and y (value)."""
    return df.rename(columns={"sale_date": "ds", "total_units_sold": "y"})


def main():
    df = get_daily_sales()
    df = prepare_for_prophet(df)

    model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=FORECAST_HORIZON_DAYS)
    forecast = model.predict(future)

    print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(FORECAST_HORIZON_DAYS))

    forecast.to_csv("forecast_output.csv", index=False)
    print("\nSaved full forecast to forecast_output.csv")


if __name__ == "__main__":
    main()
