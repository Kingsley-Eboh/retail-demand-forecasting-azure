"""
I tested the forecast for validity by holding back 90 days of real
sales, then checking it against what Prophet predicted for that
same period. I also compared Prophet against a simple baseline that
just repeats last year's numbers, to see whether the model was
actually adding value over the most basic approach possible.
"""

import os
import pymssql
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

DB_CONFIG = {
    "server": "retaildemandsqlserverus.database.windows.net",
    "user": "kingsleyadmin",
    "password": os.environ["DB_PASSWORD"],
    "database": "retaildemanddbus",
}

TOP_SELLERS = [
    ("store_2", "item_20"),
    ("store_35", "item_20"),
    ("store_12", "item_20"),
    ("store_34", "item_20"),
    ("store_12", "item_1"),
]

HOLDOUT_DAYS = 90


def get_series(store_id: str, item_id: str) -> pd.DataFrame:
    query = """
        SELECT sale_date, total_units_sold
        FROM dbo.fct_daily_sales
        WHERE store_id = %s AND item_id = %s
        ORDER BY sale_date
    """
    with pymssql.connect(**DB_CONFIG) as conn:
        return pd.read_sql(query, conn, params=(store_id, item_id))


def backtest_one(store_id: str, item_id: str) -> dict:
    df = get_series(store_id, item_id)
    df = df.rename(columns={"sale_date": "ds", "total_units_sold": "y"})

    train = df.iloc[:-HOLDOUT_DAYS]
    test = df.iloc[-HOLDOUT_DAYS:]

    model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
    model.fit(train)

    future = model.make_future_dataframe(periods=HOLDOUT_DAYS)
    forecast = model.predict(future)
    predicted = forecast.set_index("ds").loc[test["ds"], "yhat"]

    prophet_mae = mean_absolute_error(test["y"], predicted)
    prophet_mape = mean_absolute_percentage_error(test["y"], predicted)

    naive_baseline = df.set_index("ds")["y"].shift(365).loc[test["ds"]]
    naive_mae = mean_absolute_error(test["y"], naive_baseline)
    naive_mape = mean_absolute_percentage_error(test["y"], naive_baseline)

    return {
        "store_id": store_id,
        "item_id": item_id,
        "prophet_mae": round(prophet_mae, 1),
        "prophet_mape": round(prophet_mape * 100, 1),
        "naive_mae": round(naive_mae, 1),
        "naive_mape": round(naive_mape * 100, 1),
    }


def main():
    results = [backtest_one(store_id, item_id) for store_id, item_id in TOP_SELLERS]
    results_df = pd.DataFrame(results)
    print(results_df)
    results_df.to_csv("backtest_results.csv", index=False)
    print("\nsaved to backtest_results.csv")


if __name__ == "__main__":
    main()
