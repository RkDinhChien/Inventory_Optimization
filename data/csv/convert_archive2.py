import pandas as pd
from datetime import timedelta

# Đường dẫn file gốc
TRAIN_PATH = "data/csv/archive-2/train.csv"
MEAL_PATH = "data/csv/archive-2/meal_info.csv"

# Đường dẫn file output
OUTPUT_PATH = "data/csv/orders_converted.csv"

# Đọc dữ liệu
train = pd.read_csv(TRAIN_PATH)
meal_info = pd.read_csv(MEAL_PATH)

# Mapping meal_id -> dish_name (dùng category + cuisine)
def get_dish_name(row):
    meal = meal_info[meal_info["meal_id"] == row["meal_id"]]
    if not meal.empty:
        return f"{meal.iloc[0]['category']}_{meal.iloc[0]['cuisine']}"
    return f"meal_{row['meal_id']}"

train["dish_name"] = train.apply(get_dish_name, axis=1)

# Chuyển week -> date (giả sử tuần 1 là 2024-01-01, mỗi tuần tăng 7 ngày)
START_DATE = pd.to_datetime("2024-01-01")
train["date"] = train["week"].apply(lambda w: START_DATE + timedelta(days=(w-1)*7))

# Đổi tên cột
train.rename(columns={"num_orders": "quantity_sold"}, inplace=True)

# Chọn các cột cần thiết cho hệ thống
cols = ["date", "dish_name", "quantity_sold", "checkout_price", "base_price", "emailer_for_promotion", "homepage_featured"]
orders = train[cols]

# Xuất ra file mới
orders.to_csv(OUTPUT_PATH, index=False)

print(f"Đã chuyển đổi xong! File lưu tại: {OUTPUT_PATH}")
