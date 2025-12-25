"""
LUỒNG LOGIC CỦA HỆ THỐNG - GIẢI THÍCH CHI TIẾT
Từ dữ liệu → Dự đoán → Tính toán
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    LUỒNG LOGIC HỆ THỐNG                                   ║
║                  (Data Flow & Reasoning)                                   ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

print("""
📊 BƯỚC 1: DỮ LIỆU ĐẦU VÀO (INPUT DATA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hệ thống cần 3 loại dữ liệu:
─────────────────────────────

1️⃣  LỊCH SỬ ĐẠT MÓN (Orders History):
   
   File: orders.csv hoặc orders_real.csv
   Format:
   ┌─────────────┬────────────────┬───────────────┐
   │ date        │ dish_name      │ quantity_sold │
   ├─────────────┼────────────────┼───────────────┤
   │ 2023-01-01  │ Pho Bo         │ 45            │
   │ 2023-01-01  │ Banh Mi        │ 32            │
   │ 2023-01-02  │ Pho Bo         │ 52            │
   │ 2023-01-02  │ Com Tam        │ 28            │
   │ ...         │ ...            │ ...           │
   └─────────────┴────────────────┴───────────────┘
   
   Ý nghĩa:
   • Lịch sử bán hàng trong quá khứ
   • Càng nhiều data (6 tháng - 1 năm) càng tốt
   • Dùng để PHÂN TÍCH PATTERN (xu hướng)

2️⃣  CÔNG THỨC MÓN ĂN (Recipes):
   
   File: recipes.csv
   Format:
   ┌────────────────┬──────────────────┬──────────────────┐
   │ dish_name      │ material_name    │ quantity_per_dish│
   ├────────────────┼──────────────────┼──────────────────┤
   │ Pho Bo         │ Beef Sirloin     │ 0.2 kg           │
   │ Pho Bo         │ Rice Noodles     │ 0.15 kg          │
   │ Pho Bo         │ Green Onion      │ 0.03 kg          │
   │ Banh Mi        │ Baguette         │ 1 piece          │
   │ Banh Mi        │ Pork Belly       │ 0.1 kg           │
   │ ...            │ ...              │ ...              │
   └────────────────┴──────────────────┴──────────────────┘
   
   Ý nghĩa:
   • Mỗi món ăn cần nguyên liệu gì
   • Cần bao nhiêu để làm 1 phần
   • Dùng để TÍNH TOÁN nguyên liệu sau khi có forecast

3️⃣  TỒN KHO HIỆN TẠI (Current Inventory):
   
   File: current_inventory.csv
   Format:
   ┌──────────────────┬──────────────┬────────────┬──────────────┐
   │ material_name    │ current_stock│ unit_cost  │ expiry_date  │
   ├──────────────────┼──────────────┼────────────┼──────────────┤
   │ Beef Sirloin     │ 25 kg        │ $45.37/kg  │ 2025-12-20   │
   │ Rice Noodles     │ 10 kg        │ $3.50/kg   │ 2025-12-25   │
   │ Green Onion      │ 2 kg         │ $8.00/kg   │ 2025-12-15   │
   │ Baguette         │ 50 pieces    │ $1.20/pc   │ 2025-12-12   │
   │ ...              │ ...          │ ...        │ ...          │
   └──────────────────┴──────────────┴────────────┴──────────────┘
   
   Ý nghĩa:
   • Hiện tại trong kho có gì
   • Còn bao nhiêu
   • Giá bao nhiêu (tính chi phí)
   • Hết hạn khi nào (check expiry)
   • Dùng để SO SÁNH với nhu cầu → biết cần mua gì
""")

print("""
🤖 BƯỚC 2: DỰ ĐOÁN ĐƠN HÀNG (DEMAND FORECASTING)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Input: LỊCH SỬ ĐẠT MÓN (Bước 1.1)
Output: DỰ ĐOÁN cho N ngày tới

Câu hỏi: "7 ngày tới sẽ bán được bao nhiêu phần mỗi món?"
──────────────────────────────────────────────────────────

PHƯƠNG PHÁP 1: STATISTICAL (Thống kê đơn giản)
───────────────────────────────────────────────

Lý do dự đoán dựa trên:
~~~~~~~~~~~~~~~~~~~~~~

1. Trung bình lịch sử (Historical Average):
   
   Ví dụ: Phở Bò
   • 30 ngày qua: Bán trung bình 50 phần/ngày
   • Dự đoán: Ngày mai cũng sẽ ~50 phần
   
   Công thức: μ = (Σ quantity_sold) / số ngày

2. Xu hướng theo mùa (Seasonal Pattern):
   
   Ví dụ:
   • Thứ 2-5: Trung bình 45 phần
   • Thứ 6-7: Trung bình 65 phần (tăng 44%)
   • Chủ nhật: Trung bình 40 phần (giảm 11%)
   
   Công thức: s = μ_ngày_đó / μ_overall

3. Cuối tuần vs Ngày thường (Weekend Factor):
   
   Ví dụ:
   • Weekday: x1.0 (bình thường)
   • Weekend: x1.3 (tăng 30%)
   
   Công thức: w = 1.3 if weekend else 1.0

📐 Công thức tổng hợp:
~~~~~~~~~~~~~~~~~~~~

   y = μ × s × w
   
   Trong đó:
   • y = Dự đoán cho ngày cụ thể
   • μ = Trung bình lịch sử
   • s = Hệ số mùa vụ
   • w = Hệ số cuối tuần

Ví dụ cụ thể: Dự đoán Thứ 7 tuần sau
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   Dữ liệu:
   • μ = 50 phần/ngày (trung bình overall)
   • s = 1.3 (Thứ 7 thường cao hơn 30%)
   • w = 1.3 (weekend bonus)
   
   Tính toán:
   y = 50 × 1.3 × 1.3 = 84.5 ≈ 85 phần
   
   → Dự đoán Thứ 7 sẽ bán 85 phần Phở Bò

Ưu điểm:
• Nhanh (0.1 giây)
• Đơn giản, dễ hiểu
• Độ chính xác 75-80%

Nhược điểm:
• Không học được pattern phức tạp
• Không tính được tương quan giữa các món
• Không adapt với trend mới


PHƯƠNG PHÁP 2: MACHINE LEARNING (XGBoost)
──────────────────────────────────────────

Lý do dự đoán dựa trên:
~~~~~~~~~~~~~~~~~~~~~~

1. Time-based features (Đặc trưng thời gian):
   
   • day_of_week (0-6): Thứ mấy trong tuần
   • day_of_month (1-31): Ngày mấy trong tháng
   • month (1-12): Tháng mấy trong năm
   • quarter (1-4): Quý mấy
   • week_of_year (1-52): Tuần thứ mấy trong năm
   • day_of_year (1-365): Ngày thứ mấy trong năm
   • is_weekend (0/1): Có phải cuối tuần không
   
   → Học được pattern theo ngày/tuần/tháng/quý

2. Cyclical features (Đặc trưng vòng tròn):
   
   • day_sin, day_cos: Sin/Cos của ngày (vòng lặp 7 ngày)
   • month_sin, month_cos: Sin/Cos của tháng (vòng lặp 12 tháng)
   
   Ví dụ:
   • Thứ 7 (day 6) → day_sin = sin(2π×6/7) = 0.78
                    → day_cos = cos(2π×6/7) = -0.62
   
   → Giúp model hiểu "Chủ nhật gần Thứ 2" (cyclical)

3. Calendar events (Sự kiện lịch):
   
   • is_month_start (0/1): Đầu tháng (ngày 1-5)
   • is_month_end (0/1): Cuối tháng (ngày 26-31)
   • is_quarter_start: Đầu quý
   • is_quarter_end: Cuối quý
   • is_year_start: Đầu năm
   • is_year_end: Cuối năm
   
   → Học được pattern đặc biệt (lương về, cuối tháng nhiều khách)

🌲 XGBoost hoạt động như thế nào?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 1: Build Decision Trees
   
   Tree 1: Học pattern cơ bản
   ┌─────────────────────┐
   │ Is weekend?         │
   │  Yes ↓      No ↓    │
   │  +15       -5       │  (Adjustment to base)
   └─────────────────────┘

   Tree 2: Học thêm pattern
   ┌─────────────────────┐
   │ Is month_end?       │
   │  Yes ↓      No ↓    │
   │  +8        0        │
   └─────────────────────┘
   
   ... (100-1000 trees)

Step 2: Combine predictions
   
   Base = 50 phần (average)
   + Tree1 = +15 (weekend)
   + Tree2 = +8 (month end)
   + Tree3 = +3 (evening)
   + ...
   ─────────────────
   Final = 76 phần

Step 3: Learn from errors
   
   • Nếu dự đoán 76, thực tế 80 → Error = +4
   • Tree tiếp theo focus vào fix error này
   • Gradient boosting: Mỗi tree sửa lỗi của tree trước

📊 Ví dụ cụ thể: Dự đoán Thứ 7 tuần sau (XGBoost)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Input features:
   • day_of_week = 5 (Thứ 7)
   • day_of_month = 14
   • month = 12 (tháng 12)
   • quarter = 4
   • is_weekend = 1
   • day_sin = 0.78
   • day_cos = -0.62
   • month_sin = 0.0
   • month_cos = 1.0
   • is_month_start = 0
   • is_month_end = 0
   • ... (17 features total)

XGBoost processing:
   1. Base prediction: 50 phần
   2. Tree 1: +12 (weekend detected)
   3. Tree 2: +5 (mid-month)
   4. Tree 3: +8 (December season)
   5. Tree 4: +3 (Saturday specific)
   6. Tree 5: -2 (not month end)
   ... 100 trees total
   
   Final: 50 + 12 + 5 + 8 + 3 - 2 + ... = 82 phần

→ XGBoost dự đoán 82 phần (vs Statistical 85)

Ưu điểm:
• Độ chính xác 90-95%
• Học được pattern phức tạp
• Auto feature importance
• Handle non-linear relationships

Nhược điểm:
• Chậm (5-10 giây training)
• Cần nhiều data (6+ tháng)
• Black box (khó giải thích)


KẾT QUẢ BƯỚC 2:
───────────────

Output: Demand Forecast DataFrame
┌─────────────┬────────────────┬──────────────┐
│ date        │ dish_name      │ predicted_qty│
├─────────────┼────────────────┼──────────────┤
│ 2025-12-12  │ Pho Bo         │ 52           │
│ 2025-12-12  │ Banh Mi        │ 38           │
│ 2025-12-12  │ Com Tam        │ 45           │
│ 2025-12-13  │ Pho Bo         │ 48           │
│ 2025-12-13  │ Banh Mi        │ 35           │
│ ...         │ ...            │ ...          │
│ 2025-12-18  │ Pho Bo         │ 82           │  ← 7 ngày tới
│ 2025-12-18  │ Banh Mi        │ 65           │
│ 2025-12-18  │ Com Tam        │ 70           │
└─────────────┴────────────────┴──────────────┘

→ Biết rõ mỗi ngày cần chuẩn bị bao nhiêu phần mỗi món!
""")

print("""
📦 BƯỚC 3: TÍNH NGUYÊN LIỆU CẦN THIẾT (MATERIAL REQUIREMENTS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Input:
   1. DỰ ĐOÁN ĐƠN HÀNG (từ Bước 2)
   2. CÔNG THỨC MÓN ĂN (từ Bước 1.2)

Output: DANH SÁCH NGUYÊN LIỆU CẦN THIẾT

Quy trình tính toán:
───────────────────

Step 1: Aggregate demand (Tổng hợp nhu cầu)
   
   Từ forecast của 7 ngày:
   ┌────────────────┬───────────────────┐
   │ dish_name      │ total_servings    │
   ├────────────────┼───────────────────┤
   │ Pho Bo         │ 380 servings      │  (52+48+55+...+82)
   │ Banh Mi        │ 280 servings      │
   │ Com Tam        │ 320 servings      │
   └────────────────┴───────────────────┘

Step 2: Multiply với recipe (Nhân với công thức)
   
   Ví dụ: Pho Bo
   ─────────────
   
   Recipe (1 serving):
   • Beef Sirloin: 0.2 kg
   • Rice Noodles: 0.15 kg
   • Green Onion: 0.03 kg
   
   Need (380 servings):
   • Beef Sirloin: 380 × 0.2 = 76 kg
   • Rice Noodles: 380 × 0.15 = 57 kg
   • Green Onion: 380 × 0.03 = 11.4 kg

Step 3: Sum across all dishes (Tổng hợp tất cả món)
   
   Beef Sirloin:
   • Pho Bo cần: 76 kg
   • Com Tam cần: 64 kg (320 × 0.2)
   • Banh Mi cần: 0 kg (không dùng)
   ─────────────────────
   TOTAL: 140 kg

   Rice Noodles:
   • Pho Bo cần: 57 kg
   • Com Tam cần: 0 kg
   • Banh Mi cần: 0 kg
   ─────────────────────
   TOTAL: 57 kg
   
   ... (tương tự cho tất cả nguyên liệu)

KẾT QUẢ BƯỚC 3:
───────────────

Output: Material Requirements DataFrame
┌──────────────────┬─────────────────────┐
│ material_name    │ total_material_needed│
├──────────────────┼─────────────────────┤
│ Beef Sirloin     │ 140.0 kg            │
│ Rice Noodles     │ 57.0 kg             │
│ Green Onion      │ 11.4 kg             │
│ Baguette         │ 280 pieces          │
│ Pork Belly       │ 28.0 kg             │
│ ...              │ ...                 │
└──────────────────┴─────────────────────┘

→ Biết rõ cần bao nhiêu từng loại nguyên liệu!
""")

print("""
🔄 BƯỚC 4: TÍNH LƯỢNG CẦN NHẬP (RESTOCKING CALCULATION)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Input:
   1. NGUYÊN LIỆU CẦN THIẾT (từ Bước 3)
   2. TỒN KHO HIỆN TẠI (từ Bước 1.3)

Output: DANH SÁCH CẦN MUA + CHI PHÍ

Quy trình tính toán:
───────────────────

Step 1: So sánh nhu cầu vs tồn kho
   
   Ví dụ: Beef Sirloin
   ───────────────────
   
   • Cần: 140 kg (từ Bước 3)
   • Có: 25 kg (current stock)
   • Thiếu: 140 - 25 = 115 kg
   
   → CẦN MUA 115 kg

Step 2: Tính chi phí
   
   • Unit cost: $45.37/kg (từ inventory)
   • Quantity: 115 kg
   • Total cost: 115 × $45.37 = $5,217.55

Step 3: Check tất cả nguyên liệu
   
   ┌──────────────────┬───────┬──────┬────────┬──────────┐
   │ material_name    │ Need  │ Have │ Shortage│ Cost     │
   ├──────────────────┼───────┼──────┼────────┼──────────┤
   │ Beef Sirloin     │ 140kg │ 25kg │ 115kg  │ $5,217.55│
   │ Rice Noodles     │ 57kg  │ 10kg │ 47kg   │ $164.50  │
   │ Green Onion      │ 11.4kg│ 2kg  │ 9.4kg  │ $75.20   │
   │ Baguette         │ 280pc │ 50pc │ 230pc  │ $276.00  │
   │ Pork Belly       │ 28kg  │ 30kg │ 0kg    │ $0.00    │✓
   └──────────────────┴───────┴──────┴────────┴──────────┘
   
   Note: Pork Belly đủ rồi → KHÔNG cần mua

KẾT QUẢ BƯỚC 4:
───────────────

Output 1: Restocking List
┌──────────────────┬───────────────┬─────────────┐
│ material_name    │ restock_amount│ restock_cost│
├──────────────────┼───────────────┼─────────────┤
│ Beef Sirloin     │ 115.0 kg      │ $5,217.55   │
│ Rice Noodles     │ 47.0 kg       │ $164.50     │
│ Green Onion      │ 9.4 kg        │ $75.20      │
│ Baguette         │ 230 pieces    │ $276.00     │
└──────────────────┴───────────────┴─────────────┘

Output 2: Summary
• Items to restock: 4
• Total investment: $5,733.25
• Avg cost/item: $1,433.31

→ Biết rõ cần mua gì, bao nhiêu, tốn bao nhiêu tiền!
""")

print("""
⏰ BƯỚC 5 (BONUS): CHECK HẾT HẠN (EXPIRY MANAGEMENT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Input: TỒN KHO HIỆN TẠI (từ Bước 1.3)
Output: CẢNH BÁO HẾT HẠN + GỢI Ý MÓN

Quy trình:
─────────

Step 1: Tìm hàng gần hết hạn (< 5 ngày)
   
   Hôm nay: 2025-12-11
   
   ┌──────────────────┬─────────┬──────────────┬───────────┐
   │ material_name    │ stock   │ expiry_date  │ days_left │
   ├──────────────────┼─────────┼──────────────┼───────────┤
   │ Green Onion      │ 2 kg    │ 2025-12-15   │ 4 days ⚠️ │
   │ Baguette         │ 50 pc   │ 2025-12-12   │ 1 day  🔴│
   │ Beef Sirloin     │ 25 kg   │ 2025-12-20   │ 9 days ✅ │
   └──────────────────┴─────────┴──────────────┴───────────┘
   
   → 2 items cần ưu tiên dùng!

Step 2: Gợi ý món ăn sử dụng hàng đó
   
   Baguette (1 day left) → Dùng cho món nào?
   ────────────────────────────────────────
   
   Check recipes:
   • Banh Mi: Cần 1 baguette/serving
     → Current stock: 50 → Max 50 servings
   
   Green Onion (4 days left) → Dùng cho món nào?
   ─────────────────────────────────────────────
   
   Check recipes:
   • Pho Bo: Cần 0.03 kg/serving
     → Current stock: 2kg → Max 66 servings
   • Com Tam: Cần 0.02 kg/serving
     → Current stock: 2kg → Max 100 servings

Step 3: Tính priority score
   
   • Urgency: Càng gần hết hạn càng cao
   • Quantity: Càng nhiều tồn càng ưu tiên dùng
   • Usage: Món nào dùng nhiều nguyên liệu đó
   
   Score = (5 - days_left) × stock × usage_rate

KẾT QUẢ BƯỚC 5:
───────────────

Output 1: Near-Expiry Alert
⚠️ 2 materials expiring within 5 days

Output 2: Recommended Dishes
┌────────────────┬──────────────┬───────────────┬───────┐
│ dish_name      │ material_used│ max_servings  │ score │
├────────────────┼──────────────┼───────────────┼───────┤
│ Banh Mi        │ Baguette     │ 50 servings   │ 95.2  │
│ Com Tam        │ Green Onion  │ 100 servings  │ 78.5  │
│ Pho Bo         │ Green Onion  │ 66 servings   │ 65.3  │
└────────────────┴──────────────┴───────────────┴───────┘

→ Nên ưu tiên làm Banh Mi để tận dụng Baguette!
""")

print("""
🔄 TỔNG KẾT: TOÀN BỘ LUỒNG LOGIC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  📊 INPUT DATA                                                     │
│  ├─ Orders History (orders.csv)         [1]                       │
│  ├─ Recipes (recipes.csv)                [2]                       │
│  └─ Current Inventory (current_inventory.csv)  [3]                │
│                                                                    │
│                           ↓                                        │
│                                                                    │
│  🤖 BƯỚC 2: DEMAND FORECASTING                                     │
│  ├─ Input: [1] Orders History                                     │
│  ├─ Method: Statistical HOẶC XGBoost                              │
│  │  • Phân tích pattern: weekday/weekend, seasonal, trend         │
│  │  • Statistical: y = μ × s × w                                  │
│  │  • XGBoost: ŷ = Σ f_k(X) với 17 features                      │
│  └─ Output: Forecast 7 ngày tới (380 Pho, 280 Banh Mi, ...)      │
│                                                                    │
│                           ↓                                        │
│                                                                    │
│  📦 BƯỚC 3: MATERIAL REQUIREMENTS                                  │
│  ├─ Input: Forecast từ Bước 2 + [2] Recipes                       │
│  ├─ Calculation:                                                  │
│  │  • Pho Bo: 380 servings × 0.2kg beef = 76kg beef              │
│  │  • Com Tam: 320 servings × 0.2kg beef = 64kg beef             │
│  │  • Total beef needed = 140kg                                   │
│  └─ Output: Materials list (140kg beef, 57kg noodles, ...)       │
│                                                                    │
│                           ↓                                        │
│                                                                    │
│  🔄 BƯỚC 4: RESTOCKING CALCULATION                                 │
│  ├─ Input: Materials từ Bước 3 + [3] Current Inventory           │
│  ├─ Calculation:                                                  │
│  │  • Beef: Need 140kg - Have 25kg = Buy 115kg                   │
│  │  • Cost: 115kg × $45.37 = $5,217.55                           │
│  └─ Output: Shopping list + Total cost $5,733.25                 │
│                                                                    │
│                           ↓                                        │
│                                                                    │
│  ⏰ BƯỚC 5: EXPIRY MANAGEMENT                                      │
│  ├─ Input: [3] Current Inventory                                  │
│  ├─ Check: Hàng nào hết hạn < 5 ngày?                            │
│  │  • Baguette: 1 day left (urgent!)                             │
│  │  • Green Onion: 4 days left (warning)                         │
│  └─ Output: Recommend Banh Mi (dùng Baguette gần hết hạn)        │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

KEY INSIGHTS:
────────────

✓ Dữ liệu đầu vào: 3 files (orders, recipes, inventory)

✓ Dự đoán dựa trên: Lịch sử + Pattern (weekday/weekend, seasonal)
  • Statistical: Trung bình × Hệ số mùa × Hệ số cuối tuần
  • XGBoost: 17 features → 100 decision trees → Học pattern phức tạp

✓ Tính nguyên liệu: Forecast × Recipe = Materials needed

✓ Tính lượng nhập: Materials needed - Current stock = Buy amount

✓ Bonus: Check expiry → Recommend dishes để tránh lãng phí
""")

print("""
💡 VÍ DỤ THỰC TẾ: CHẠY HỆ THỐNG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scenario: Quán Phở ABC - Lập kế hoạch cho tuần tới
──────────────────────────────────────────────────

INPUT:
─────

1. Orders History: 6 tháng data (Phở Bò, Bánh Mì, Cơm Tấm)
   • Thứ 2-5: Trung bình 150 phần/ngày
   • Thứ 6-7: Trung bình 220 phần/ngày
   • Chủ nhật: Trung bình 180 phần/ngày

2. Recipes:
   • Phở Bò: 0.2kg beef, 0.15kg noodles, 0.03kg onion
   • Bánh Mì: 1 baguette, 0.1kg pork, 0.05kg veggies
   • Cơm Tấm: 0.2kg pork, 0.15kg rice, 0.1kg veggies

3. Current Inventory:
   • Beef: 25kg (cost $45/kg, expires Dec 20)
   • Noodles: 10kg
   • Baguette: 50pc (expires Dec 12 - TOMORROW!)
   • Pork: 30kg
   • Rice: 20kg

PROCESSING:
───────────

Bước 2: Forecast (XGBoost)
   • Thứ 5-6 (Dec 12-13): Weekday → 150 phần/ngày
   • Thứ 7-CN (Dec 14-15): Weekend → 220 phần/ngày
   • Thứ 2-4 (Dec 16-18): Weekday → 150 phần/ngày
   
   7 days total:
   • Phở Bò: 380 servings
   • Bánh Mì: 280 servings
   • Cơm Tấm: 320 servings

Bước 3: Materials
   • Beef: 380×0.2 = 76kg (chỉ Phở)
   • Noodles: 380×0.15 = 57kg
   • Baguette: 280×1 = 280pc
   • Pork: (280×0.1)+(320×0.2) = 92kg
   • Rice: 320×0.15 = 48kg
   • Onion: 380×0.03 = 11.4kg
   • Veggies: (280×0.05)+(320×0.1) = 46kg

Bước 4: Restocking
   • Beef: Need 76kg - Have 25kg = Buy 51kg ($2,314)
   • Noodles: Need 57kg - Have 10kg = Buy 47kg ($165)
   • Baguette: Need 280pc - Have 50pc = Buy 230pc ($276)
   • Pork: Need 92kg - Have 30kg = Buy 62kg ($1,860)
   • Rice: Need 48kg - Have 20kg = Buy 28kg ($56)
   • Onion: Need 11.4kg - Have 0kg = Buy 11.4kg ($91)
   • Veggies: Need 46kg - Have 0kg = Buy 46kg ($184)
   
   TOTAL COST: $4,946

Bước 5: Expiry Alert
   ⚠️ Baguette expires TOMORROW (50pc in stock)
   
   Recommendation:
   → Làm thêm Bánh Mì hôm nay!
   → Có thể làm 50 phần Bánh Mì (dùng hết 50 baguette)
   → Hoặc giảm giá promotion để bán nhanh

OUTPUT:
───────

Action Items cho Manager:
1. ✅ Đặt hàng ngay: 51kg beef, 47kg noodles, 230 baguette, 62kg pork, 
   28kg rice, 11.4kg onion, 46kg veggies
2. ✅ Budget: Chuẩn bị $4,946
3. ⚠️ Ưu tiên làm Bánh Mì hôm nay (50 baguette hết hạn)
4. 📊 Expect: ~980 servings tuần tới (140/day average)

→ Manager có đầy đủ thông tin để ra quyết định!
""")
