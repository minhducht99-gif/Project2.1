import pandas as pd
import matplotlib.pyplot as plt

# đọc dữ liệu
df = pd.read_csv("bid_rigging_df.csv")

# làm sạch dữ liệu
df["Market"] = df["Market"].str.strip()

# chuyển sang dạng số
df["WWBID"] = pd.to_numeric(df["WWBID"], errors="coerce")
df["LFWBID"] = pd.to_numeric(df["LFWBID"], errors="coerce")
df["LFCBID"] = pd.to_numeric(df["LFCBID"], errors="coerce")

# tính giá trung bình
avg_price = df.groupby(["Market","Year"])[["WWBID","LFWBID","LFCBID"]].mean().reset_index()

print(avg_price)

# vẽ biểu đồ
markets = avg_price["Market"].unique()

for m in markets:

    data = avg_price[avg_price["Market"] == m]

    plt.figure(figsize=(10,6))

    plt.plot(data["Year"], data["WWBID"], marker="o", label="Whole Milk")
    plt.plot(data["Year"], data["LFWBID"], marker="o", label="Low Fat White")
    plt.plot(data["Year"], data["LFCBID"], marker="o", label="Low Fat Chocolate")

    plt.title(f"Average Winning Price - {m}")
    plt.xlabel("Year")
    plt.ylabel("Average Price")

    plt.legend()
    plt.grid(True)

    plt.show()