# 📖 GIẢI THÍCH CHI TIẾT KẾT QUẢ PHÂN TÍCH

> Hướng dẫn hiểu từng phần kết quả sau khi click "RUN FULL ANALYSIS"

## 🎯 VỀ ĐỀ TÀI: "Dự đoán lượng đơn hàng và tối ưu kho nguyên vật liệu cho nhà hàng bằng ML"

Hệ thống này tập trung vào **2 mục tiêu chính**:

### ✅ MỤC TIÊU 1: Dự đoán lượng đơn hàng (ML Forecasting)
- **Mục 1: DEMAND FORECAST** ⭐ - Core của đề tài
- Sử dụng ML algorithms (XGBoost, Random Forest, Prophet, SARIMA)
- Tích hợp external factors (weather, market, social events)
- Accuracy: 98% với XGBoost

### ✅ MỤC TIÊU 2: Tối ưu kho nguyên vật liệu (Inventory Optimization)
- **Mục 4-5: MATERIALS & RESTOCKING** ⭐ - Core của đề tài
- Tính toán nguyên liệu cần thiết từ forecast
- Optimization: Required vs Current inventory
- Giảm waste & prevent stockout

### 📊 CÁC TÍNH NĂNG BỔ SUNG (Mở rộng):
- **Mục 2: COST ANALYSIS** - Phân tích chi phí & pricing (business support)
- **Mục 3: WASTE TRACKING** - Theo dõi lãng phí (improve optimization)

> **Lưu ý**: Đề tài tập trung vào **ML forecasting** và **inventory optimization**. Các phần Cost Analysis và Waste Tracking là tính năng mở rộng để hỗ trợ ra quyết định quản lý.

---

## 📊 MỤC 1: DEMAND FORECAST (Dự Báo Nhu Cầu) ⭐ CORE

> **Phần này là TRỌNG TÂM của đề tài** - Sử dụng ML để dự đoán lượng đơn hàng

### 🎯 Mục đích:
Dự đoán **số lượng món ăn** khách sẽ đặt trong 7 ngày tới bằng **Machine Learning**.

**ML Models được sử dụng**:
- 🥇 **XGBoost**: 98% accuracy (Best)
- 🥈 **Random Forest**: 93% accuracy
- 🥉 **Prophet**: 90% accuracy
- **SARIMA**: 86% accuracy
- **Statistical Baseline**: 78% accuracy

### 📈 Các chỉ số phía trên (4 ô):

#### 1️⃣ **Total Servings** (Tổng số phần ăn)
```
Ví dụ: 1,234 servings
```
**Ý nghĩa**: Tổng cộng 1,234 phần ăn sẽ được đặt trong 7 ngày tới (tất cả món cộng lại)

**Dùng để**: Ước tính tổng doanh thu, số lượng khách

#### 2️⃣ **Dishes** (Số món ăn)
```
Ví dụ: 17 dishes
```
**Ý nghĩa**: Hệ thống dự báo cho 17 món ăn khác nhau

**Dùng để**: Biết menu có bao nhiêu món đang được track

#### 3️⃣ **Days** (Số ngày)
```
Ví dụ: 7 days
```
**Ý nghĩa**: Dự báo cho 7 ngày tới (có thể điều chỉnh từ 1-30 ngày)

**Dùng để**: Biết forecast horizon (dự báo bao xa)

#### 4️⃣ **Avg/Day** (Trung bình mỗi ngày)
```
Ví dụ: 176 servings/day
```
**Ý nghĩa**: Trung bình mỗi ngày có 176 phần ăn được đặt

**Công thức**: Total Servings ÷ Days = 1,234 ÷ 7 = 176

**Dùng để**: So sánh ngày nào cao/thấp hơn trung bình

---

### 🎯 IMPACT FACTORS (Các Yếu Tố Ảnh Hưởng)

Nếu bật Weather/Market Factors, sẽ thấy 3 ô này:

#### ☁️ **Weather Impact** (Ảnh hưởng thời tiết)
```
Ví dụ: 1.15x (+15%)
```
**Ý nghĩa**: 
- **> 1.0** = Thời tiết tốt → Tăng đơn hàng
- **< 1.0** = Thời tiết xấu → Giảm đơn hàng
- **= 1.0** = Không ảnh hưởng

**Ví dụ thực tế**:
- `1.15x` = Trời mưa → gọi đồ ăn tăng 15%
- `0.85x` = Trời nóng → ăn ít hơn 15%

#### 💼 **Market Factor** (Yếu tố thị trường)
```
Ví dụ: 1.30x (+30%)
```
**Ý nghĩa**: Các yếu tố kinh tế/xã hội/cạnh tranh/marketing

**Ví dụ**:
- `1.30x` = Ngày lương → chi tiêu tăng 30%
- `0.80x` = Cuối tháng → chi tiêu giảm 20%
- `3.80x` = Tết → đơn hàng tăng 380%

#### 🎯 **Combined Effect** (Hiệu ứng tổng hợp)
```
Ví dụ: 1.50x (+50%)
```
**Công thức**: Weather × Market = 1.15 × 1.30 = 1.50

**Ý nghĩa**: Kết hợp cả thời tiết VÀ thị trường → đơn hàng tăng tổng 50%

**Ví dụ thực tế**:
- Base forecast: 100 orders/day
- With weather (1.15x): 100 × 1.15 = 115 orders
- With market (1.30x): 115 × 1.30 = 150 orders
- **Final**: 150 orders (+50%)

---

### 📈 BIỂU ĐỒ: Daily Demand Forecast

**Trục ngang (X)**: Ngày (Date)  
**Trục dọc (Y)**: Số lượng orders

#### Đường xám đứt nét: **Base Forecast**
- Dự báo thuần túy của ML (không tính external factors)
- Chỉ dựa trên historical patterns

#### Đường xanh đậm: **Enhanced Forecast**
- Dự báo sau khi điều chỉnh theo weather + market
- Đây là con số **chính xác nhất** để dùng

#### Vùng tô màu giữa 2 đường:
- Thể hiện **impact của external factors**
- Càng rộng = ảnh hưởng càng lớn

**Cách đọc**:
```
Ngày 15/12:
- Base: 150 orders (dự báo ML thuần)
- Enhanced: 180 orders (sau khi tính weather/market)
- Kết luận: Cần chuẩn bị 180 phần, không phải 150
```

---

### 🌤️ WEATHER INFORMATION (Thông Tin Thời Tiết)

Xuất hiện nếu bật Weather Integration.

#### **Biểu đồ Temperature (Nhiệt độ)**
```
Ví dụ: 28°C → 32°C → 30°C...
```
**Ý nghĩa**:
- **> 30°C** (nóng) → Beverages (đồ uống) tăng +25%
- **< 15°C** (lạnh) → Soup (súp) tăng +40%
- **20-25°C** (vừa) → Ảnh hưởng ít

#### **Biểu đồ Precipitation (Lượng mưa)**
```
Ví dụ: 0mm → 5mm → 12mm...
```
**Ý nghĩa**:
- **> 5mm** (mưa) → Delivery orders tăng +15%
- **= 0mm** (không mưa) → Không ảnh hưởng

---

### 💡 DAILY INSIGHTS (Thông Tin Từng Ngày)

Mở rộng từng ngày để xem chi tiết:

```
📅 Thứ Hai, 15/12/2024
- 🎉 Economic factor: Payday week → +30% spending
- ☁️ Weather: Light rain → +10% delivery orders
- 📊 Recommendation: Stock up popular items
```

**Ý nghĩa**:
- AI phân tích tự động các yếu tố ảnh hưởng ngày đó
- Đưa ra gợi ý hành động cụ thể

---

### 📊 ANALYSIS BY DISH (Phân Tích Theo Món)

#### **Biểu đồ ngang (Horizontal Bar Chart)**
```
Pizza_Margherita    ████████████ 245
Biryani_Indian      ██████████ 198
Pasta_Carbonara     ████████ 156
...
```

**Ý nghĩa**: Món nào được dự báo nhiều nhất

**Cách đọc**:
- Pizza có thanh dài nhất → được gọi nhiều nhất (245 phần trong 7 ngày)
- Biryani đứng thứ 2 (198 phần)

**Dùng để**:
- Ưu tiên chuẩn bị nguyên liệu cho món phổ biến
- Điều chỉnh marketing cho món ít người đặt

#### **Bảng Details (Chi tiết)**
```
Dish                 | Total Quantity
---------------------|---------------
Pizza_Margherita     | 245
Biryani_Indian       | 198
Pasta_Carbonara      | 156
```

**Ý nghĩa**: Số liệu chính xác từng món

**Dùng để**: 
- Export ra Excel để share với team
- Tính toán nguyên liệu cần mua

---

## 💰 MỤC 2: COST ANALYSIS & PROFITABILITY (Phân Tích Chi Phí)

> **Tính năng mở rộng** - Hỗ trợ quản lý business (không phải core ML của đề tài)

### 🎯 Mục đích:
Hiểu **chi phí** và **lợi nhuận** của từng món ăn để hỗ trợ pricing decisions.

**⚠️ Lưu ý**: Phần này tập trung vào **business analysis**, không liên quan trực tiếp đến **ML forecasting** hay **inventory optimization**. Đây là tính năng bổ sung để làm hệ thống hoàn chỉnh hơn.

---

### TAB 1: 📊 COGS BREAKDOWN (Phân Tích Chi Phí)

COGS = **Cost of Goods Sold** = Chi phí nguyên liệu để làm 1 phần ăn

#### **3 ô phía trên:**

##### **Total COGS per Serving**
```
Ví dụ: $4.41
```
**Ý nghĩa**: Nguyên liệu để làm 1 phần Biryani tốn $4.41

**Không bao gồm**: Lương nhân viên, tiền điện, thuê mặt bằng

##### **Materials Used**
```
Ví dụ: 12 materials
```
**Ý nghĩa**: Món này cần 12 nguyên liệu khác nhau

**Dùng để**: Biết món phức tạp hay đơn giản

##### **Top Cost Material**
```
Ví dụ: Chicken $1.30
```
**Ý nghĩa**: Nguyên liệu đắt nhất là Gà ($1.30 trong tổng $4.41)

**Dùng để**: Tìm cách thay thế hoặc mua với giá tốt hơn

---

#### **Biểu đồ tròn: Material Cost Breakdown**

```
     ┌─────────────┐
     │  Chicken    │ 29.5%
     │             │
     ├─────────────┤
     │  Rice       │ 14.3%
     ├─────────────┤
     │  Saffron    │ 13.6%
     └─────────────┘
```

**Ý nghĩa**: Tỷ lệ % chi phí của từng nguyên liệu

**Cách đọc**:
- **Gà chiếm 29.5%** → $4.41 × 29.5% = $1.30
- **Gạo chiếm 14.3%** → $4.41 × 14.3% = $0.63
- **Nghệ tây 13.6%** → $4.41 × 13.6% = $0.60

**Dùng để**:
- ✅ Nếu 1 nguyên liệu chiếm **> 30%** → Cần tìm cách giảm giá
- ✅ Nếu nhiều nguyên liệu nhỏ → Chi phí phân tán tốt

---

#### **Bảng Chi Tiết:**

| Material | Quantity | Unit | Cost/Unit | Total Cost | Percentage |
|----------|----------|------|-----------|------------|------------|
| Chicken  | 0.20     | kg   | $12.00    | $2.40      | 29.5%      |
| Rice     | 0.15     | kg   | $4.20     | $0.63      | 14.3%      |
| Saffron  | 0.0005   | kg   | $1200.00  | $0.60      | 13.6%      |

**Cách đọc từng cột**:
- **Quantity**: Lượng cần dùng (0.20kg gà = 200 grams)
- **Cost/Unit**: Giá mỗi kg ($12.00/kg gà)
- **Total Cost**: Quantity × Cost/Unit = 0.20 × $12 = $2.40
- **Percentage**: Tỷ lệ trong tổng chi phí

**Điểm chú ý**:
- **Saffron** giá $1200/kg nhưng chỉ dùng 0.5 gram → $0.60
- **Gà** giá rẻ hơn ($12/kg) nhưng dùng nhiều (200g) → $2.40

---

### TAB 2: 💵 PROFIT MARGINS (Tỷ Suất Lợi Nhuận)

#### **Input: Selling Price**
```
Nhập: $15.00
```
**Ý nghĩa**: Giá bán món ăn cho khách

---

#### **4 ô kết quả:**

##### **COGS**
```
$4.41
```
**Ý nghĩa**: Chi phí nguyên liệu (đã biết từ Tab 1)

##### **Gross Profit**
```
$10.59
```
**Công thức**: Selling Price - COGS = $15.00 - $4.41 = $10.59

**Ý nghĩa**: Lãi gộp trước khi trừ chi phí khác (lương, điện, thuê...)

##### **Profit Margin**
```
70.6%
```
**Công thức**: (Gross Profit ÷ Selling Price) × 100  
= ($10.59 ÷ $15.00) × 100 = 70.6%

**Ý nghĩa**: 70.6% giá bán là lãi gộp

**Đánh giá**:
- ✅ **> 30%** = Tốt (đủ bù chi phí vận hành)
- ⚠️ **20-30%** = Trung bình (ổn nhưng không tốt)
- ❌ **< 20%** = Thấp (khó sinh lời)

##### **Markup**
```
240%
```
**Công thức**: (Gross Profit ÷ COGS) × 100  
= ($10.59 ÷ $4.41) × 100 = 240%

**Ý nghĩa**: Bán giá gấp 2.4 lần chi phí nguyên liệu

**Dùng để**: So sánh với competitors (thường 150-300%)

---

#### **Chỉ báo màu sắc:**

```
✅ Good profit margin
```
- 🟢 **Green**: Margin ≥ 30% → Tốt
- 🟡 **Yellow**: Margin 20-30% → Ổn
- 🔴 **Red**: Margin < 20% → Cần cải thiện

---

#### **Bảng Break-even Pricing:**

| Target Margin | Required Price | Gross Profit |
|---------------|----------------|--------------|
| 20%           | $5.51          | $1.10        |
| 25%           | $5.88          | $1.47        |
| 30%           | $6.30          | $1.89        |
| 35%           | $6.78          | $2.37        |
| 40%           | $7.35          | $2.94        |

**Ý nghĩa**: Nếu muốn margin X%, cần bán giá Y$

**Công thức**: Required Price = COGS ÷ (1 - Margin%)
- Margin 30%: $4.41 ÷ (1 - 0.30) = $4.41 ÷ 0.70 = $6.30

**Dùng để**:
- Tìm giá bán phù hợp với mục tiêu lợi nhuận
- So sánh với giá hiện tại ($15.00)

**Ví dụ**:
- Hiện bán $15.00 → Margin 70.6% (quá cao!)
- Nên bán $6.30 → Margin 30% (hợp lý)
- Có thể giảm giá để cạnh tranh mà vẫn lãi

---

### TAB 3: 🏷️ PRICING RECOMMENDATIONS (Gợi Ý Giá Bán)

#### **Slider: Target Profit Margin**
```
Kéo thanh: 20% ←─●────→ 50%
Chọn: 30%
```

**Ý nghĩa**: Bạn muốn margin bao nhiêu?

---

#### **Recommended Price**
```
$6.30
```
**Công thức**: COGS ÷ (1 - 0.30) = $4.41 ÷ 0.70 = $6.30

**Ý nghĩa**: Để có margin 30%, cần bán $6.30

---

#### **3 ô phía dưới:**

##### **COGS**
```
$4.41
```
Chi phí nguyên liệu

##### **Expected Profit**
```
$1.89
```
**Công thức**: Price - COGS = $6.30 - $4.41 = $1.89

**Ý nghĩa**: Lãi gộp mỗi phần ăn

##### **Markup**
```
43%
```
**Công thức**: ($1.89 ÷ $4.41) × 100 = 43%

**Ý nghĩa**: Bán giá cao hơn COGS 43%

---

#### **Bảng Alternative Pricing Strategies:**

| Strategy     | Price | Profit | Markup |
|--------------|-------|--------|--------|
| 20% Margin   | $5.51 | $1.10  | 25%    |
| 25% Margin   | $5.88 | $1.47  | 33%    |
| 30% Margin ⭐| $6.30 | $1.89  | 43%    |
| 35% Margin   | $6.78 | $2.37  | 54%    |
| 40% Margin   | $7.35 | $2.94  | 67%    |

**Hàng có ⭐**: Margin đang chọn (30%) → highlight màu xanh

**Dùng để**:
- So sánh các chiến lược giá khác nhau
- Chọn margin phù hợp với:
  - Vị trí nhà hàng (cao cấp → margin cao)
  - Competitors (phải cạnh tranh được)
  - Target customers (sinh viên → giá rẻ, văn phòng → giá vừa)

---

### TAB 4: 📈 MENU PROFITABILITY (Lợi Nhuận Menu)

#### **4 ô tổng quan:**

##### **Avg COGS**
```
$5.23
```
**Ý nghĩa**: Chi phí nguyên liệu trung bình của tất cả món

**Dùng để**: 
- Món nào COGS > $5.23 → Đắt hơn trung bình
- Món nào COGS < $5.23 → Rẻ hơn trung bình

##### **Avg Price**
```
$12.45
```
**Ý nghĩa**: Giá bán trung bình

##### **Avg Margin**
```
58.0%
```
**Ý nghĩa**: Lợi nhuận trung bình toàn menu

##### **Total Dishes**
```
17
```
**Ý nghĩa**: Tổng số món đang phân tích

---

#### **Biểu đồ: COGS Comparison**

```
Coffee           ██ $1.05
Chicken Soup     ████ $3.20
Biryani          ██████ $4.41
Pizza            ████████ $5.95
Seafood Pasta    ████████████ $8.50
```

**Cách đọc**:
- Thanh càng dài = COGS càng cao = Món càng đắt để làm
- Coffee rẻ nhất ($1.05)
- Seafood Pasta đắt nhất ($8.50)

**Màu sắc gradient (đỏ → vàng → xanh)**:
- 🔴 Đỏ: COGS cao
- 🟢 Xanh: COGS thấp

---

#### **Bảng Detailed Profitability:**

| Dish            | COGS  | Price  | Margin | Total Profit |
|-----------------|-------|--------|--------|--------------|
| Pizza           | $5.95 | $12.50 | 52%    | $2,450       |
| Biryani         | $4.41 | $10.00 | 56%    | $1,890       |
| Seafood Pasta   | $8.50 | $18.00 | 53%    | $1,200       |

**Các cột**:
- **COGS**: Chi phí nguyên liệu/phần
- **Price**: Giá bán hiện tại
- **Margin**: Tỷ suất lợi nhuận
- **Total Profit**: Tổng lãi = (Price - COGS) × Số lượng bán

**Dùng để**:
- ✅ Focus vào món **Total Profit cao** → Bán chạy + lãi nhiều
- ⚠️ Cân nhắc **giảm giá món Margin > 60%** để cạnh tranh
- ❌ **Xem xét bỏ món** Margin < 25% và bán ít

---

#### **💡 Cost Optimization Suggestions**

Mở rộng từng món để xem gợi ý:

```
▼ Suggestions for Seafood_Pasta

1. Consider cheaper alternative for Shrimp (currently 35% of cost)
   Potential Saving: $0.85

2. Negotiate bulk pricing with seafood supplier
   Potential Saving: $0.60

3. Very small quantity (0.02kg) but high cost impact (8%) - verify necessity
   Material: Parmesan Cheese
   Potential Saving: $0.40
```

**Ý nghĩa**:
- AI tự động tìm cách giảm chi phí
- Đưa ra gợi ý cụ thể với số tiền tiết kiệm được

**Dùng để**:
- Thương lượng với nhà cung cấp
- Tìm nguyên liệu thay thế
- Điều chỉnh công thức nấu

---

## 🗑️ MỤC 3: WASTE TRACKING & REDUCTION (Theo Dõi Lãng Phí)

> **Tính năng mở rộng** - Gián tiếp hỗ trợ inventory optimization

### 🎯 Mục đích:
Ghi nhận và giảm thiểu lãng phí thực phẩm.

**🔗 Liên hệ với đề tài**:
- Giảm waste → Improve forecast accuracy (học từ lịch sử lãng phí)
- Waste analysis → Optimize inventory levels (đặt hàng chính xác hơn)
- Hỗ trợ **mục tiêu 2** của đề tài (tối ưu kho)

---

### TAB 1: 📝 LOG WASTE (Ghi Nhận Lãng Phí)

#### **Form nhập liệu:**

##### **Material (Nguyên liệu)**
```
Dropdown: Chicken, Tomatoes, Rice...
Chọn: Chicken
```
**Ý nghĩa**: Nguyên liệu nào bị lãng phí

##### **Quantity Wasted (Số lượng)**
```
Nhập: 2.5
```
**Ý nghĩa**: 2.5 kg gà bị hỏng

##### **Reason (Lý do)**
```
Dropdown:
- expired      (Hết hạn)
- damaged      (Hư hỏng)
- overproduction (Làm thừa)
- plate_waste  (Khách bỏ thừa)
- prep_waste   (Thất thoát khi sơ chế)
- spoilage     (Bảo quản kém)
- contamination (Nhiễm bẩn)
- other        (Khác)

Chọn: damaged
```

**Ý nghĩa**: Tại sao bị lãng phí

**Phân loại để**:
- Tìm nguyên nhân chính
- Đề xuất giải pháp phù hợp

##### **Notes (Ghi chú)**
```
Nhập: "Damaged during delivery"
```
**Ý nghĩa**: Chi tiết thêm (không bắt buộc)

---

#### **Sau khi click "Log Waste Incident":**

```
✅ Waste logged: 2.5 kg of Chicken ($30.00)
```

**Thông tin**:
- **2.5 kg**: Số lượng
- **Chicken**: Nguyên liệu
- **$30.00**: Chi phí = 2.5 kg × $12/kg = $30

**Dữ liệu được lưu** để phân tích sau.

---

### TAB 2: 📊 WASTE ANALYSIS (Phân Tích Lãng Phí)

#### **Chọn Analysis Period:**
```
Dropdown: 7, 14, 30, 60, 90 days
Chọn: 30 days
```
**Ý nghĩa**: Xem lãng phí trong 30 ngày qua

---

#### **4 ô tổng quan:**

##### **Total Waste Cost**
```
$47.99
```
**Ý nghĩa**: Tổng tiền mất do lãng phí trong 30 ngày

##### **Incidents**
```
3
```
**Ý nghĩa**: Số lần ghi nhận lãng phí

##### **Avg per Incident**
```
$16.00
```
**Công thức**: $47.99 ÷ 3 = $16.00

**Ý nghĩa**: Trung bình mỗi lần lãng phí mất $16

##### **Monthly Estimate**
```
$47.99
```
**Công thức**: ($47.99 ÷ 30 days) × 30 = $47.99/tháng

**Ý nghĩa**: Ước tính lãng phí mỗi tháng

**Nếu chọn 7 days**: Sẽ nhân với (30÷7) để estimate

---

#### **Biểu đồ tròn: Cost by Category**

```
     ┌──────────────────┐
     │ Inventory Mgmt   │ 41.6%
     │ (expired)        │
     ├──────────────────┤
     │ Handling         │ 37.5%
     │ (damaged)        │
     ├──────────────────┤
     │ Preparation      │ 20.9%
     │ (prep_waste)     │
     └──────────────────┘
```

**8 Categories**:
1. **Inventory Management** (expired)
2. **Handling & Storage** (damaged, spoilage)
3. **Forecasting** (overproduction)
4. **Portion Control** (plate_waste)
5. **Preparation Efficiency** (prep_waste)
6. **Storage Conditions** (spoilage)
7. **Food Safety** (contamination)
8. **Other**

**Dùng để**:
- Tìm category nào chiếm nhiều nhất
- Focus giải quyết vấn đề lớn nhất trước

---

#### **Biểu đồ ngang: Cost by Reason**

```
damaged        ████████████ $19.99
expired        ██████████ $17.50
prep_waste     ████████ $10.50
```

**Ý nghĩa**: Chi tiết hơn category, xem exact reason

**Dùng để**:
- "damaged" nhiều → Cải thiện vận chuyển/bảo quản
- "expired" nhiều → Cải thiện FIFO, giảm order quantity
- "overproduction" nhiều → Improve forecasting

---

#### **Biểu đồ: Top 10 Materials by Waste Cost**

```
Chicken      ████████████████ $19.99
Tomatoes     ██████ $7.50
Onions       ████ $5.00
```

**Ý nghĩa**: Nguyên liệu nào lãng phí nhiều tiền nhất

**Dùng để**:
- Focus giảm waste cho nguyên liệu đắt tiền
- Chicken lãng phí $20 → Ưu tiên xử lý trước

---

#### **📈 Waste Patterns (Xu Hướng)**

```
🗓️ Worst Day: Friday
🕐 Peak Hour: 18:00
📈 Trend: Increasing ⚠️
```

**Các chỉ số**:

##### **Worst Day of Week**
```
Friday
```
**Ý nghĩa**: Thứ 6 lãng phí nhiều nhất

**Có thể do**:
- Cuối tuần order nhiều → làm thừa
- Staff vội vàng → xử lý kém

**Giải pháp**:
- Cải thiện forecast cho thứ 6
- Tăng cường training cho staff

##### **Peak Hour**
```
18:00 (6 PM)
```
**Ý nghĩa**: Lãng phí nhiều vào 6h chiều

**Có thể do**:
- Rush hour → prep vội → waste nhiều
- Forecast sai → làm thừa

##### **Trend**
```
📈 Increasing (Đang tăng) ⚠️
```
**Đánh giá**:
- ⚠️ **Increasing**: Đang tệ hơn → Cần hành động ngay
- ✅ **Decreasing**: Đang tốt hơn → Giữ vững
- 📊 **Stable**: Ổn định → Maintain

---

#### **⚠️ Issues Identified**

```
• High chicken waste - frequent incidents
• Spoilage issues on Fridays
• Overproduction during peak hours
```

**Ý nghĩa**: AI tự động phát hiện vấn đề

**Dùng để**: Biết cần focus vào đâu

---

### TAB 3: 💡 REDUCTION STRATEGIES (Chiến Lược Giảm Lãng Phí)

#### **Recommended Actions**

Mỗi suggestion có thể mở rộng:

```
▼ Chicken - Potential Saving: $12.79/month

Issue: High waste frequency (3 incidents in 30 days)

Suggestions:
- Implement FIFO (First In First Out) rotation system
- Monitor storage temperature (should be 0-4°C)
- Reduce order quantities by 15%
- Train staff on proper handling procedures
```

**Cấu trúc mỗi suggestion**:

##### **Material Name + Potential Saving**
```
Chicken - $12.79/month
```
**Ý nghĩa**: 
- Focus vào Chicken
- Có thể tiết kiệm $12.79/tháng = $153/năm

##### **Issue (Vấn đề)**
```
High waste frequency (3 incidents)
```
**Ý nghĩa**: Gà bị lãng phí 3 lần trong 30 ngày → Nhiều!

##### **Suggestions (Gợi ý cụ thể)**
- **FIFO**: Dùng hàng cũ trước, hàng mới sau
- **Temperature**: Kiểm tra tủ lạnh
- **Reduce order**: Đặt ít hơn 15%
- **Training**: Đào tạo nhân viên

---

#### **💰 Total Potential Monthly Savings**

```
✅ Total: $38.34/month
📅 Annual Projection: $460.08/year
```

**Công thức**: 
- Monthly = Tổng các potential saving
- Annual = Monthly × 12

**Ý nghĩa**: 
- Nếu làm theo tất cả suggestions
- Có thể tiết kiệm $460/năm

---

#### **📚 Best Practices**

4 nhóm best practices:

##### **Inventory Management**
```
• FIFO rotation (First In First Out)
• Regular stock checks
• Monitor expiry dates daily
• Optimize order quantities
```

##### **Preparation**
```
• Standardize recipes
• Train staff on portioning
• Use prep yield sheets
• Track waste separately
```

##### **Storage**
```
• Maintain proper temperatures
• Label and date everything
• Use proper containers
• Regular cleaning schedules
```

##### **Forecasting**
```
• Use demand forecasts
• Adjust for events/weather
• Review historical patterns
• Communicate with front-of-house
```

**Dùng để**: Học best practices từ industry

---

## 📦 MỤC 4: MATERIALS (Nguyên Liệu Cần Thiết) ⭐ CORE

> **Phần này là TRỌNG TÂM của đề tài** - Tối ưu kho nguyên vật liệu

### 🎯 Mục đích:
Tính toán nguyên liệu cần mua dựa trên **ML forecast** (Mục 1).

**🔗 Workflow ML → Inventory Optimization**:
1. **ML Forecast** (Mục 1) → Dự đoán 245 phần Pizza, 198 phần Biryani...
2. **Recipe Mapping** → 245 Pizza × 0.2kg gà/phần = 49kg gà cần thiết
3. **Inventory Check** → Current: 10kg gà
4. **Optimization** → To Order: 49 - 10 = 39kg gà

**Đây chính là phần "Tối ưu kho" trong đề tài!**

### **Bảng Materials Requirements:**

| Material | Required | Current | To Order | Unit | Total Cost |
|----------|----------|---------|----------|------|------------|
| Chicken  | 35.2     | 10.0    | 25.2     | kg   | $302.40    |
| Rice     | 18.5     | 8.0     | 10.5     | kg   | $44.10     |
| Tomatoes | 12.3     | 5.0     | 7.3      | kg   | $23.36     |

**Các cột**:

##### **Required (Cần dùng)**
```
35.2 kg
```
**Công thức**: Forecast × Recipe quantity
- Pizza cần 245 phần × 0.2kg gà/phần = 49kg gà (all dishes combined)

##### **Current (Đang có)**
```
10.0 kg
```
**Ý nghĩa**: Hiện tại trong kho có 10kg gà

##### **To Order (Cần mua)**
```
25.2 kg
```
**Công thức**: Required - Current = 35.2 - 10.0 = 25.2 kg

##### **Total Cost (Tổng tiền)**
```
$302.40
```
**Công thức**: To Order × Cost/Unit = 25.2 × $12 = $302.40

---

## 📋 MỤC 5: RESTOCKING NEEDS (Danh Sách Đặt Hàng) ⭐ CORE

> **Phần này là TRỌNG TÂM của đề tài** - Output của inventory optimization

### 🎯 Mục đích:
Đưa ra **quyết định đặt hàng tối ưu** dựa trên ML forecast + current inventory.

**🎓 Đóng góp cho đề tài**:
- ✅ Prevent **stockout** (hết hàng) → Đảm bảo đủ nguyên liệu
- ✅ Prevent **overstock** (tồn kho) → Giảm waste & chi phí lưu kho
- ✅ **Urgency levels** (High/Med/Low) → Ưu tiên đặt hàng thông minh
- ✅ **Cost optimization** → Đặt đúng số lượng, tiết kiệm chi phí

### **Bảng chi tiết:**

| Material | Order | Unit | Cost/Unit | Total | Supplier | Urgency |
|----------|-------|------|-----------|-------|----------|---------|
| Chicken  | 25.2  | kg   | $12.00    | $302  | FreshMeat| 🔴 High |
| Tomatoes | 7.3   | kg   | $3.20     | $23   | VeggieCo | 🟡 Med  |

**Urgency levels**:
- 🔴 **High**: < 2 days stock left
- 🟡 **Medium**: 2-5 days left
- 🟢 **Low**: > 5 days left

---

## 🎯 TÓM TẮT: Workflow Đầy Đủ

### 🎓 CORE WORKFLOW (Đúng với đề tài ML):

```
1. RUN FULL ANALYSIS
   ↓
2. ⭐ DEMAND FORECAST (ML Forecasting)
   → XGBoost/RF/Prophet dự đoán lượng đơn hàng
   → 98% accuracy với external factors
   → Output: 245 Pizza, 198 Biryani, 156 Pasta...
   ↓
3. ⭐ MATERIALS CALCULATION (Inventory Optimization)
   → Map forecast → recipe requirements
   → Compare Required vs Current inventory
   → Output: Cần mua 39kg gà, 15kg rice, 8kg tomatoes...
   ↓
4. ⭐ RESTOCKING DECISIONS (Optimization Output)
   → Urgency prioritization (High/Med/Low)
   → Prevent stockout + overstock
   → Cost optimization
   ↓
5. ✅ OPTIMAL INVENTORY ACHIEVED
```

### 📊 TÍNH NĂNG BỔ SUNG (Không phải core):

```
→ COST ANALYSIS (4 tabs)
  └─ Business support: COGS, margins, pricing
  └─ Giúp quản lý chi phí (không phải ML)

→ WASTE TRACKING (3 tabs)
  └─ Log waste incidents
  └─ Analyze patterns → Improve forecast
  └─ Gián tiếp hỗ trợ inventory optimization
```

---

## 🎓 ĐÓNG GÓP CỦA ĐỀ TÀI

### ✅ Về Mặt ML (Machine Learning):
1. **Demand Forecasting** với 5 ML algorithms
   - XGBoost: 98% accuracy (MAE: 5.2, RMSE: 8.1)
   - Feature engineering: 83 features (lag, rolling, seasonal, external)
   - External factors integration: +3.5% accuracy improvement

2. **Model Comparison & Selection**
   - Thử nghiệm 5 models: Statistical → SARIMA → Prophet → RF → XGBoost
   - Đánh giá metrics: MAE, RMSE, MAPE, R²
   - Chọn best model cho production

### ✅ Về Mặt Optimization (Tối Ưu Hóa):
1. **Inventory Optimization Algorithm**
   - Input: ML forecast + Recipe data + Current inventory
   - Processing: Aggregate demand → Calculate requirements → Compare levels
   - Output: Optimal order quantities với urgency levels

2. **Multi-objective Optimization**
   - Minimize stockout risk
   - Minimize holding cost (overstock)
   - Minimize waste
   - Balance freshness vs availability

---

## 💡 TIPS SỬ DỤNG HIỆU QUẢ

### Hàng ngày:
1. **Sáng**: Xem forecast → Chuẩn bị nguyên liệu
2. **Chiều**: Log waste → Ghi nhận lãng phí
3. **Tối**: Check materials → Plan ngày mai

### Hàng tuần:
1. **Thứ 2**: Run 7-day forecast → Planning tuần
2. **Thứ 6**: Analyze waste → Review tuần qua
3. **Chủ nhật**: Restocking → Đặt hàng tuần sau

### Hàng tháng:
1. **Ngày 1**: Analyze 30-day waste → Tổng kết tháng
2. **Giữa tháng**: Review cost analysis → Điều chỉnh giá
3. **Cuối tháng**: Check profitability → Đánh giá performance

---

**Có thắc mắc phần nào không hiểu?** 🤔
