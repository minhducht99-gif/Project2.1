import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("bid_rigging_df.csv")

df["Market"] = df["Market"].str.strip()

df["KYFMO"] = pd.to_numeric(df["KYFMO"], errors="coerce")
df["WWBID"] = pd.to_numeric(df["WWBID"], errors="coerce")
df["LFWBID"] = pd.to_numeric(df["LFWBID"], errors="coerce")
df["LFCBID"] = pd.to_numeric(df["LFCBID"], errors="coerce")

df["AVGPRICE"] = df[["WWBID","LFWBID","LFCBID"]].mean(axis=1)

df = df.dropna(subset=["KYFMO","AVGPRICE"])

for market in df["Market"].unique():

    data = df[df["Market"] == market]

    x = data["KYFMO"]
    y = data["AVGPRICE"]

    # tính hồi quy
    slope, intercept = np.polyfit(x, y, 1)

    # vẽ scatter
    plt.figure(figsize=(8,6))
    plt.scatter(x, y)

    # vẽ đường hồi quy
    plt.plot(x, slope*x + intercept)

    plt.title(f"Regression: {market}")
    plt.xlabel("Cost (KYFMO)")
    plt.ylabel("Average Price")

    # hiển thị phương trình
    plt.text(min(x), max(y),
             f"y = {slope:.3f}x + {intercept:.3f}")

    plt.show()