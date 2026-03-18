import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("bid_rigging_df.csv")

# Chuẩn hóa text
df["Market"] = df["Market"].str.strip()
df["Winner"] = df["Winner"].str.strip()

# Gộp các công ty khác thành OTHER
df["COMPANY_GROUP"] = df["Winner"].apply(
    lambda x: x if x in ["MEYER", "TRAUTH"] else "OTHER"
)

# Chuyển quantity sang số
df["WWQTY"] = pd.to_numeric(df["WWQTY"], errors="coerce")
df["LFWQTY"] = pd.to_numeric(df["LFWQTY"], errors="coerce")
df["LFCQTY"] = pd.to_numeric(df["LFCQTY"], errors="coerce")

# Tổng lượng sữa
df["TOTALQTY"] = df["WWQTY"] + df["LFWQTY"] + df["LFCQTY"]

# Lọc TRI-COUNTY
df_tri = df[df["Market"] == "TRI-COUNTY"]

# Tổng thị trường mỗi năm
total_year = df_tri.groupby("Year")["TOTALQTY"].sum().reset_index()
total_year = total_year.rename(columns={"TOTALQTY":"YEAR_TOTAL"})

# Tổng theo nhóm công ty
company_year = df_tri.groupby(["Year","COMPANY_GROUP"])["TOTALQTY"].sum().reset_index()

# Ghép
merged = pd.merge(company_year, total_year, on="Year")

# Market share
merged["MARKET_SHARE"] = merged["TOTALQTY"] / merged["YEAR_TOTAL"]

# Pivot để vẽ biểu đồ
pivot = merged.pivot(index="Year", columns="COMPANY_GROUP", values="MARKET_SHARE")

pivot = pivot.fillna(0)

if "OTHER" not in pivot.columns:
    pivot["OTHER"] = 0

pivot = pivot[["MEYER","TRAUTH","OTHER"]]

# Chỉ hiện thị số nguyên
pivot.index = pivot.index.astype(int)

# Vẽ biểu đồ
pivot.plot(kind="bar", figsize=(12,6))

plt.title("Market Share in TRI-COUNTY Market")
plt.xlabel("Year")
plt.ylabel("Market Share")
plt.grid(axis="y")

# Hiển thị giá trị trên từng cột
for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        value = pivot.iloc[i, j]
        if value > 0:
            plt.text(i, value + 0.01, f"{value:.2%}", ha="center", va="bottom")
            
plt.show()