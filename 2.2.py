import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu
df = pd.read_csv("bid_rigging_df.csv")

# Chuẩn hóa dữ liệu
df["Market"] = df["Market"].str.strip()
df["Winner"] = df["Winner"].str.strip()


# Chỉ giữ các cột cần thiết
df = df[["Market", "District", "Year", "Winner"]]

# Sắp xếp dữ liệu
df = df.sort_values(["Market", "District", "Year"])

# Winner của năm trước trong cùng district
df["PrevWinner"] = df.groupby(["Market", "District"])["Winner"].shift(1)

# Kiểm tra giữ hợp đồng
df["Incumbent"] = (df["Winner"] == df["PrevWinner"]).astype(int)

# Loại bỏ năm đầu tiên của mỗi district (vì không có năm trước để so sánh)
df_valid = df.dropna(subset=["PrevWinner"])

# Tính incumbency rate theo năm và market
incumbency = df_valid.groupby(["Market", "Year"])["Incumbent"].mean().reset_index()

print("Incumbency rate table:")
print(incumbency)

# Pivot để vẽ biểu đồ
pivot_inc = incumbency.pivot(index="Year", columns="Market", values="Incumbent")

# Vẽ line chart
ax = pivot_inc.plot(marker="o", figsize=(10,6))

plt.title("Incumbency Rate Over Time")
plt.xlabel("Year")
plt.ylabel("Incumbency Rate")

plt.grid(True)
plt.xticks(rotation=0)

# Hiển thị giá trị trên điểm
for line in ax.lines:
    for x, y in zip(line.get_xdata(), line.get_ydata()):
        ax.text(x, y, f"{y:.2f}", ha="center", va="bottom")

plt.show()