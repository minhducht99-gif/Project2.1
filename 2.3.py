import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu
df = pd.read_csv("bid_rigging_df.csv")

# Chuẩn hóa text
df["Market"] = df["Market"].str.strip()

# Chuyển dữ liệu sang số
df["WWBID"] = pd.to_numeric(df["WWBID"], errors="coerce")
df["LFWBID"] = pd.to_numeric(df["LFWBID"], errors="coerce")
df["LFCBID"] = pd.to_numeric(df["LFCBID"], errors="coerce")
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")


# Tính standard deviation theo Market và Year
std_bid = df.groupby(["Market","Year"])[["WWBID","LFWBID","LFCBID"]].std().reset_index()

print(std_bid)

# -------- VẼ BIỂU ĐỒ -------- #

markets = std_bid["Market"].unique()

for m in markets:

    data = std_bid[std_bid["Market"] == m]

    plt.figure(figsize=(10,6))

    plt.plot(data["Year"], data["WWBID"], marker="o", label="Whole Milk")
    plt.plot(data["Year"], data["LFWBID"], marker="o", label="Low Fat White")
    plt.plot(data["Year"], data["LFCBID"], marker="o", label="Low Fat Chocolate")

    plt.title(f"Bid Price Standard Deviation - {m}")
    plt.xlabel("Year")
    plt.ylabel("Standard Deviation")

    plt.grid(True)
    plt.legend()

    plt.show()