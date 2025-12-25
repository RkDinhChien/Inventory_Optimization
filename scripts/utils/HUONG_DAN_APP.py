"""
HƯỚNG DẪN SỬ DỤNG WEB APP - CHI TIẾT
Step-by-step guide với screenshots mô tả
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║              HƯỚNG DẪN SỬ DỤNG WEB APP - TỪNG BƯỚC                        ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

print("""
🚀 BƯỚC 1: KHỞI ĐỘNG APP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mở Terminal và chạy:
────────────────────

    $ cd "/Users/rykan/ĐỒ ÁN/Inventory_Optimization"
    $ source .venv/bin/activate
    $ streamlit run app.py

Kết quả:
────────

    You can now view your Streamlit app in your browser.
    
    Local URL: http://localhost:8501
    Network URL: http://192.168.1.3:8501

→ App tự động mở trong browser!
→ Nếu không mở, vào: http://localhost:8501
""")

print("""
🖥️  BƯỚC 2: GIAO DIỆN APP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Khi app mở, bạn sẽ thấy:
─────────────────────────

┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  📦 Inventory Optimization System                                         │
│  ML-Powered Demand Forecasting for F&B Industry                           │
│                                                                            │
│  ┌─────────────────┐  ┌──────────────────────────────────────────────┐  │
│  │   SIDEBAR       │  │          MAIN CONTENT                        │  │
│  │   (Settings)    │  │                                              │  │
│  │                 │  │  👈 Configure settings and click             │  │
│  │  ⚙️ Settings    │  │     'Initialize System' to start            │  │
│  │  ☑ Use ML       │  │                                              │  │
│  │  📊 Algorithm   │  │  Features:                                   │  │
│  │  📅 Days        │  │  • Demand forecasting                        │  │
│  │  📁 Data        │  │  • Material requirements                     │  │
│  │                 │  │  • Restocking recommendations                │  │
│  │  🚀 Initialize  │  │  • Expiry management                         │  │
│  │                 │  │                                              │  │
│  └─────────────────┘  └──────────────────────────────────────────────┘  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

2 phần chính:
─────────────

1. SIDEBAR (Bên trái):
   • ⚙️ Settings - Cấu hình hệ thống
   • 🚀 Initialize button - Khởi động

2. MAIN CONTENT (Bên phải):
   • Hiển thị kết quả
   • Charts & tables
   • Metrics & recommendations
""")

print("""
⚙️  BƯỚC 3: CẤU HÌNH SIDEBAR (Bên trái)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Trong SIDEBAR, bạn sẽ thấy:
───────────────────────────

┌─────────────────────────┐
│  ⚙️ Settings            │
├─────────────────────────┤
│                         │
│  ☐ Use Machine Learning │  ← Checkbox 1
│                         │
│  ML Algorithm           │  ← Dropdown (nếu ML ON)
│  ▼ xgboost              │
│                         │
│  Forecast Settings      │
│  ─────────────────      │
│  Days to Forecast: 7    │  ← Slider
│  [────●────────] 1-30   │
│                         │
│  Data Source            │
│  ─────────────          │
│  ⦿ Sample Data          │  ← Radio buttons
│  ○ Real Dataset         │
│  ○ Upload Custom        │
│                         │
│  [🚀 Initialize System] │  ← Button quan trọng!
│                         │
└─────────────────────────┘

Chi tiết từng phần:
───────────────────

1️⃣  Use Machine Learning (Checkbox):
   
   ☐ OFF (unchecked):
      • Dùng Statistical method (nhanh, 75-80% accuracy)
      • Tốt cho: Testing, development, ít data
   
   ☑ ON (checked):
      • Dùng ML (chậm hơn, 90-95% accuracy)
      • Tốt cho: Production, critical decisions
   
   → Click vào checkbox để toggle ON/OFF

2️⃣  ML Algorithm (Dropdown - chỉ hiện khi ML ON):
   
   Các options:
   • xgboost       ← Recommended! (90-95% accuracy) 🏆
   • sarima        (85-90% accuracy)
   • random_forest (85-92% accuracy)
   • prophet       (85-90% accuracy)
   
   → Click dropdown, chọn algorithm

3️⃣  Days to Forecast (Slider):
   
   [────●────────] 1 ──────────────── 30
   
   • Kéo slider trái/phải
   • Hoặc click vào số để nhập trực tiếp
   • Range: 1-30 ngày
   • Default: 7 ngày
   
   Khuyến nghị:
   • 7 days: Weekly planning (phổ biến nhất)
   • 14 days: Bi-weekly planning
   • 30 days: Monthly planning

4️⃣  Data Source (Radio buttons):
   
   ⦿ Sample Data:
      • 5 món ăn mẫu
      • 1830 orders (1 năm data)
      • Tốt cho: Demo, testing
   
   ○ Real Dataset (archive-2):
      • 17 món ăn thực
      • 2395 records (119M+ orders)
      • 2.8 năm data từ food delivery
      • Tốt cho: Production, accurate predictions
   
   ○ Upload Custom:
      • Upload CSV của bạn
      • Format: date, dish_name, quantity_sold
   
   → Click vào radio button để chọn

5️⃣  🚀 Initialize System (Button):
   
   • Button MÀU XANH lớn
   • Click để khởi động hệ thống
   • Sẽ load data và chuẩn bị model
   
   Khi click:
   ✅ Loading data...
   ✅ Initializing optimizer...
   ✅ System initialized!
   
   → Sau đó 4 buttons mới xuất hiện ở main content!
""")

print("""
🎮 BƯỚC 4: SỬ DỤNG 4 BUTTONS CHÍNH (Sau khi Initialize)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sau khi click "Initialize System", 4 buttons xuất hiện:
────────────────────────────────────────────────────────

┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  [📈 Generate Forecast] [📦 Calculate Materials]              │
│                                                                │
│  [🔄 Get Restocking]    [🔄 Run Full Analysis]               │
│                                                                │
└────────────────────────────────────────────────────────────────┘

Chức năng từng button:
──────────────────────

1️⃣  📈 Generate Forecast:
   
   Chức năng:
   • Dự đoán nhu cầu cho N ngày tới
   • Tính số lượng từng món cần chuẩn bị
   
   Khi click:
   ✅ Generating forecast...
   → Hiển thị:
      • Total servings (tổng phần ăn)
      • Forecast by dish (chi tiết từng món)
      • Line chart (biểu đồ theo ngày)
      • Bar chart (top dishes)
   
   Ví dụ output:
   ┌─────────────────────────────────────────┐
   │ 📊 DEMAND FORECAST                      │
   ├─────────────────────────────────────────┤
   │ Total Servings:  828                    │
   │ Dishes:          5                      │
   │ Forecast Days:   7                      │
   │ Avg/Day:         118                    │
   ├─────────────────────────────────────────┤
   │ [Line Chart: Daily Demand →]            │
   │ [Bar Chart: Top Dishes →]               │
   │ [Table: Forecast Details]               │
   └─────────────────────────────────────────┘

2️⃣  📦 Calculate Materials:
   
   Chức năng:
   • Tính nguyên liệu cần thiết
   • Dựa trên forecast đã generate
   
   ⚠️ Phải click "Generate Forecast" TRƯỚC!
   
   Khi click:
   ✅ Calculating materials...
   → Hiển thị:
      • Materials needed (số loại nguyên liệu)
      • Total units (tổng số lượng)
      • Top 10 materials chart
      • Material details table
   
   Ví dụ output:
   ┌─────────────────────────────────────────┐
   │ 📦 MATERIAL REQUIREMENTS                │
   ├─────────────────────────────────────────┤
   │ Materials Needed:  12                   │
   │ Total Units:       350.5                │
   ├─────────────────────────────────────────┤
   │ [Bar Chart: Top Materials →]            │
   │                                         │
   │ Mixed Vegetables   66.6 units           │
   │ Tomato Sauce      63.6 units           │
   │ Chicken Breast    41.5 units           │
   │ ...                                     │
   └─────────────────────────────────────────┘

3️⃣  🔄 Get Restocking:
   
   Chức năng:
   • Xem nguyên liệu nào cần nhập thêm
   • Tính chi phí nhập hàng
   
   ⚠️ Phải click "Calculate Materials" TRƯỚC!
   
   Khi click:
   ✅ Optimizing restocking...
   → Hiển thị:
      • Items to restock (số món cần nhập)
      • Total investment (tổng chi phí)
      • Restocking costs chart
      • Restocking list table
   
   Ví dụ output:
   ┌─────────────────────────────────────────┐
   │ 🔄 RESTOCKING RECOMMENDATIONS           │
   ├─────────────────────────────────────────┤
   │ Items to Restock:    5                  │
   │ Total Investment:    $2,068.82          │
   │ Avg Cost/Item:       $413.76            │
   ├─────────────────────────────────────────┤
   │ [Bar Chart: Costs by Material →]        │
   │                                         │
   │ Chicken Breast   $826.20  (20kg)       │
   │ Beef Sirloin     $680.50  (15kg)       │
   │ ...                                     │
   └─────────────────────────────────────────┘

4️⃣  🔄 Run Full Analysis:
   
   Chức năng:
   • Chạy TẤT CẢ 3 steps trên cùng lúc
   • One-click solution!
   
   Khi click:
   ✅ Running full analysis...
   → Tự động:
      1. Generate forecast
      2. Calculate materials
      3. Get restocking
   
   → Hiển thị TẤT CẢ kết quả cùng lúc!
   
   💡 Tip: Dùng button này cho nhanh nhất!

Thứ tự khuyến nghị:
───────────────────

Option A (Step-by-step - Học từng bước):
1. Click "Generate Forecast" → Xem results
2. Click "Calculate Materials" → Xem results
3. Click "Get Restocking" → Xem results

Option B (Fast - Nhanh nhất):
1. Click "Run Full Analysis" → Xem tất cả!

→ Recommend Option B cho người mới!
""")

print("""
📊 BƯỚC 5: ĐỌC KẾT QUẢ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sau khi chạy analysis, bạn sẽ thấy nhiều sections:
──────────────────────────────────────────────────

1. 📈 DEMAND FORECAST Section:
   ────────────────────────────
   
   Metrics (4 numbers ở top):
   ┌──────────────┬──────────────┬──────────────┬──────────────┐
   │ Total        │ Dishes       │ Forecast     │ Avg/Day      │
   │ Servings     │              │ Days         │              │
   │ 828          │ 5            │ 7            │ 118          │
   └──────────────┴──────────────┴──────────────┴──────────────┘
   
   Ý nghĩa:
   • Total Servings: Tổng số phần ăn cần chuẩn bị
   • Dishes: Số món khác nhau
   • Forecast Days: Dự đoán cho mấy ngày
   • Avg/Day: Trung bình mỗi ngày
   
   Charts:
   • Line Chart: Xem trend theo ngày
     → Hover chuột lên để xem chi tiết
     → Zoom in/out bằng mouse wheel
   
   • Bar Chart: Xem top dishes
     → Món nào bán nhiều nhất?
   
   Table: Chi tiết từng món
   → Scroll để xem tất cả

2. 📦 MATERIAL REQUIREMENTS Section:
   ─────────────────────────────────
   
   Metrics:
   ┌──────────────┬──────────────┬──────────────┐
   │ Materials    │ Total Units  │ Est. Cost    │
   │ Needed       │              │ (if shown)   │
   │ 12           │ 350.5        │ $1,250       │
   └──────────────┴──────────────┴──────────────┘
   
   Bar Chart: Top 10 materials
   • Hover để xem số chính xác
   • Nguyên liệu nào cần nhiều nhất?
   
   Table: Full material list
   • Scroll để xem tất cả
   • Check từng nguyên liệu cần bao nhiêu

3. 🔄 RESTOCKING Section:
   ─────────────────────
   
   Nếu CÓ cần restock:
   ┌──────────────┬──────────────┬──────────────┐
   │ Items to     │ Total        │ Avg Cost/    │
   │ Restock      │ Investment   │ Item         │
   │ 5            │ $2,068.82    │ $413.76      │
   └──────────────┴──────────────┴──────────────┘
   
   • Chart: Chi phí từng món
   • Table: Danh sách cần mua
     → Material name
     → Current stock (hiện có)
     → Shortage (thiếu bao nhiêu)
     → Cost (giá mua)
   
   Nếu KHÔNG cần restock:
   ✅ All materials are sufficient!
   → Không cần mua thêm gì

4. ⏰ NEAR-EXPIRY MATERIALS Section:
   ──────────────────────────────────
   
   Nếu CÓ hàng gần hết hạn:
   ⚠️ 2 materials expiring within 5 days
   
   • Chart: Days until expiry
     → Màu đỏ = urgent (1-2 ngày)
     → Màu vàng = warning (3-4 ngày)
     → Màu xanh = ok (5+ ngày)
   
   • Table: Expiry details
     → Material name
     → Stock (còn bao nhiêu)
     → Days left (còn mấy ngày)
     → Expiry date (ngày hết hạn)
   
   • 💡 Recommended Dishes:
     → Gợi ý món nào dùng được hàng gần hết hạn
     → Dish name
     → Max servings (làm được tối đa bao nhiêu)
     → Score (điểm ưu tiên)
   
   Nếu KHÔNG có hàng gần hết hạn:
   ✅ No materials expiring soon!
   → Inventory tốt!
""")

print("""
💡 BƯỚC 6: TIPS & TRICKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Charts (Biểu đồ):
─────────────────

✅ Interactive! Có thể:
   • Hover: Di chuột lên để xem chi tiết
   • Zoom: Mouse wheel để zoom in/out
   • Pan: Click + drag để di chuyển
   • Reset: Double-click để reset view
   • Download: Icon 📷 ở góc để save ảnh

Tables (Bảng):
──────────────

✅ Có thể:
   • Scroll: Cuộn lên/xuống xem hết
   • Sort: Click vào column header để sắp xếp
   • Search: Một số table có search box

Settings Changes:
─────────────────

Nếu muốn thay đổi settings:
1. Thay đổi trong sidebar
2. Click "Initialize System" lại
3. Click "Run Full Analysis" lại
→ Sẽ có kết quả mới!

Compare Methods:
────────────────

Muốn so sánh Statistical vs ML?

Test 1: Statistical
1. ☐ Uncheck "Use ML"
2. Initialize
3. Run analysis
4. Note: Total servings = 830

Test 2: XGBoost
1. ☑ Check "Use ML"
2. Select "xgboost"
3. Initialize
4. Run analysis
5. Note: Total servings = 747

→ So sánh 2 kết quả!

Performance:
────────────

Statistical:
• Fast: ~0.5 seconds
• Use for: Quick estimates

XGBoost:
• Slower: ~5-10 seconds (training)
• Use for: Accurate predictions

Stop App:
─────────

Trong terminal:
• Nhấn Ctrl + C
• App sẽ dừng
""")

print("""
🔥 BƯỚC 7: WORKFLOW THỰC TẾ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scenario 1: WEEKLY PLANNING (Phổ biến nhất)
────────────────────────────────────────────

Mỗi Thứ 2 đầu tuần:

1. Mở app: streamlit run app.py

2. Configure (Sidebar):
   ☑ Use Machine Learning
   ▼ xgboost
   Days to Forecast: 7
   ⦿ Real Dataset

3. Click: 🚀 Initialize System

4. Click: 🔄 Run Full Analysis

5. Đọc kết quả:
   • Forecast: Cần chuẩn bị bao nhiêu
   • Materials: Nguyên liệu cần gì
   • Restocking: Cần mua gì, bao nhiêu tiền
   • Expiry: Hàng nào gần hết hạn

6. Action:
   • In restocking list → Đưa cho purchasing
   • Check expiry list → Ưu tiên dùng trước
   • Save forecast → Planning cho team

→ Done! Mất 5 phút!

Scenario 2: QUICK ESTIMATE (Nhanh)
───────────────────────────────────

Cần số liệu gấp cho meeting:

1. Mở app

2. Configure (Sidebar):
   ☐ Use Machine Learning OFF (nhanh)
   Days: 7
   ⦿ Sample Data

3. Initialize → Run Full Analysis

4. Screenshot kết quả → Present

→ Done trong 2 phút!

Scenario 3: MONTHLY PLANNING (Chi tiết)
────────────────────────────────────────

Đầu tháng, plan cho cả tháng:

1. Configure:
   ☑ ML ON
   Days: 30
   ⦿ Real Dataset

2. Run analysis

3. Export/Save:
   • Screenshot all charts
   • Copy tables to Excel
   • Analyze trends

4. Plan:
   • Bulk ordering (mua sỉ)
   • Negotiate với suppliers
   • Budget allocation

→ Comprehensive planning!

Scenario 4: COMPARING ALGORITHMS
─────────────────────────────────

Test xem algorithm nào tốt:

Test 1: Statistical
→ Initialize → Run → Note results

Test 2: XGBoost
→ Change algorithm → Initialize → Run → Compare

Test 3: SARIMA
→ Change algorithm → Initialize → Run → Compare

→ Pick best performer!
""")

print("""
❓ TROUBLESHOOTING (Xử lý lỗi)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lỗi 1: "Connection error" / Không load được
────────────────────────────────────────────

Giải pháp:
1. Check terminal có lỗi gì không
2. Refresh browser (F5 hoặc Cmd+R)
3. Đóng tab, mở lại: http://localhost:8501

Lỗi 2: "No module named 'streamlit'"
─────────────────────────────────────

Giải pháp:
$ source .venv/bin/activate
$ pip install streamlit plotly

Lỗi 3: ML not available / ML failed
───────────────────────────────────

Giải pháp:
1. ☐ Uncheck "Use ML"
2. Use Statistical method (fallback)

Hoặc:
$ source .venv/bin/activate
$ pip install statsmodels xgboost scikit-learn prophet

Lỗi 4: App chạy chậm
────────────────────

Giải pháp:
• ☐ Turn OFF ML (dùng Statistical)
• Giảm forecast days (7 thay vì 30)
• Use Sample Data (nhẹ hơn Real Dataset)

Lỗi 5: "Calculate Materials" không hoạt động
─────────────────────────────────────────────

Nguyên nhân: Chưa generate forecast

Giải pháp:
1. Click "Generate Forecast" TRƯỚC
2. Sau đó mới click "Calculate Materials"

Hoặc:
→ Click "Run Full Analysis" (làm tất cả!)

Lỗi 6: Port 8501 đã được dùng
─────────────────────────────

Giải pháp:
$ lsof -ti:8501 | xargs kill
$ streamlit run app.py
""")

print("""
✅ TÓM TẮT - QUICK START
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5 BƯỚC ĐƠN GIẢN:
─────────────────

1. Khởi động:
   $ streamlit run app.py

2. Configure Sidebar:
   ☑ Use ML (hoặc ☐ nếu muốn nhanh)
   Days: 7
   Data: Real Dataset

3. Initialize:
   Click 🚀 "Initialize System"

4. Run Analysis:
   Click 🔄 "Run Full Analysis"

5. Đọc kết quả:
   • 📈 Forecast
   • 📦 Materials
   • 🔄 Restocking
   • ⏰ Expiry

→ DONE! Mất 5 phút!

KEY POINTS:
───────────

✓ Sidebar = Settings (cấu hình)
✓ Main = Results (kết quả)
✓ 4 buttons = 4 functions
✓ "Run Full Analysis" = One-click solution
✓ Charts = Interactive (hover, zoom)
✓ ML = Chậm nhưng chính xác (90-95%)
✓ Statistical = Nhanh nhưng ổn (75-80%)

💡 PRO TIP:
───────────

Lần đầu dùng:
→ ☐ ML OFF, Sample Data, 7 days
→ "Run Full Analysis"
→ Làm quen với giao diện

Sau khi quen:
→ ☑ ML ON, Real Dataset, 7-30 days
→ "Run Full Analysis"
→ Use cho production!
""")

print("""
🎯 CÒN THẮC MẮC?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Chạy các demo để hiểu rõ hơn:
─────────────────────────────

$ python demo_quick.py          # Statistical demo
$ python demo_comparison.py     # So sánh methods
$ python demo_explanation.py    # Giải thích hệ thống
$ python demo_backtesting_simple.py  # Độ chính xác
$ python demo_regression.py     # Công thức
$ python demo_strategy.py       # Khi nào dùng gì

Hoặc hỏi tôi:
─────────────

"Làm sao để..."
"Tại sao..."
"Khi nào dùng..."

→ Tôi sẽ giải thích chi tiết! 🎓
""")
