"""
I built this chart to show the backtest results visually, since the
gap between Prophet and the naive baseline is easier to see than
to read off a table.
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("backtest_results.csv")
df["label"] = df["store_id"] + " / " + df["item_id"]

x = range(len(df))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar([i - width/2 for i in x], df["prophet_mape"], width, label="Prophet")
ax.bar([i + width/2 for i in x], df["naive_mape"], width, label="Naive baseline")

ax.set_xlabel("Store / Item")
ax.set_ylabel("MAPE (%)")
ax.set_title("Forecast Accuracy: Prophet vs Naive Baseline")
ax.set_xticks(list(x))
ax.set_xticklabels(df["label"], rotation=15)
ax.legend()

plt.tight_layout()
plt.savefig("backtest_comparison.png")
print("Saved chart to backtest_comparison.png")
