"""
Demo: Công Thức Dự Đoán - Có Dùng Regression Không?
Giải thích chi tiết toán học đằng sau ML forecasting
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║           CÔNG THỨC DỰ ĐOÁN - REGRESSION & MACHINE LEARNING              ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

print("""
❓ CÂU HỎI: "Công thức dự đoán là gì? Có dùng regression không?"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ CÂU TRẢ LỜI: CÓ! Tất cả đều dùng regression (dự đoán số liên tục)

Nhưng có nhiều LOẠI regression khác nhau:
  1. Linear Regression (đơn giản)
  2. Tree-based Regression (Random Forest, XGBoost)
  3. Time Series Regression (SARIMA, Prophet)
""")

print("""
📊 1. STATISTICAL METHOD (Simple Linear Approach)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Công thức:
──────────

    y = μ × s × w
    
    Trong đó:
    • y = predicted quantity (số lượng dự đoán)
    • μ = historical mean (trung bình lịch sử)
    • s = seasonal_factor (hệ số mùa)
    • w = weekend_factor (hệ số cuối tuần)

Ví dụ cụ thể:
─────────────

    Data lịch sử: Pasta Marinara bán trung bình 50 phần/ngày
    
    Dự đoán cho Thứ 7, tháng 12 (mùa đông):
    
    μ = 50 (trung bình)
    s = 1.1 (mùa đông +10%)
    w = 1.2 (cuối tuần +20%)
    
    y = 50 × 1.1 × 1.2 = 66 phần
    
    ✓ Đây là Linear Regression đơn giản (chỉ nhân hệ số)
    ✗ Không học được patterns phức tạp
    ✗ Giả định relationship là linear (tuyến tính)
""")

print("""
🎯 2. XGBOOST (Gradient Boosted Regression Trees)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Công thức tổng quát:
────────────────────

    ŷ = f(X) = Σ(k=1 to K) f_k(X)
    
    Trong đó:
    • ŷ = predicted value
    • X = feature vector [x₁, x₂, ..., x₁₇]
    • f_k = tree thứ k
    • K = số trees (thường 100-1000 trees)

Chi tiết hơn:
─────────────

    ŷ = f₁(X) + f₂(X) + f₃(X) + ... + f_K(X)
    
    Mỗi tree f_k học từ "residual" (sai số) của tree trước:
    
    Tree 1: f₁(X) → dự đoán ban đầu
    Residual 1: r₁ = y_actual - f₁(X)
    
    Tree 2: f₂(X) → học từ r₁
    Residual 2: r₂ = r₁ - f₂(X)
    
    Tree 3: f₃(X) → học từ r₂
    ...
    
    Kết quả cuối: ŷ = Σ(k=1 to K) f_k(X)

Feature vector X (17 features):
───────────────────────────────

    X = [
        day_of_week,      # 0-6 (Mon-Sun)
        day_of_month,     # 1-31
        month,            # 1-12
        quarter,          # 1-4
        week_of_year,     # 1-52
        day_of_year,      # 1-365
        is_weekend,       # 0 or 1
        day_sin,          # sin(2π × day/365)
        day_cos,          # cos(2π × day/365)
        month_sin,        # sin(2π × month/12)
        month_cos,        # cos(2π × month/12)
        is_month_start,   # 0 or 1
        is_month_end,     # 0 or 1
        is_quarter_start, # 0 or 1
        is_quarter_end,   # 0 or 1
        is_year_start,    # 0 or 1
        is_year_end       # 0 or 1
    ]

Ví dụ cụ thể:
─────────────

    Dự đoán cho ngày 15/12/2024 (Chủ nhật):
    
    X = [6, 15, 12, 4, 50, 350, 1, 0.95, 0.31, 0.0, 1.0, 0, 0, 0, 0, 0, 0]
    
    Tree 1: Kiểm tra "is_weekend == 1" → +12 phần
    Tree 2: Kiểm tra "month == 12" → +5 phần
    Tree 3: Kiểm tra "day_of_month == 15" → +3 phần
    ...
    Tree 100: Tổng hợp tất cả → +2 phần
    
    ŷ = 50 (base) + 12 + 5 + 3 + ... + 2 = 72 phần
    
    ✓ Non-linear regression (không tuyến tính)
    ✓ Học được interactions phức tạp
    ✓ Tự động feature importance
""")

print("""
🌲 3. CHI TIẾT VỀ DECISION TREE REGRESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mỗi tree là một hàm phân đoạn (piecewise function):

    f(X) = {
        w₁, if X ∈ Region₁
        w₂, if X ∈ Region₂
        w₃, if X ∈ Region₃
        ...
    }

Ví dụ Decision Tree:
────────────────────

                    [Root: is_weekend?]
                    /                 \\
                Yes (1)              No (0)
                /                      \\
        [month >= 11?]          [day_of_week >= 5?]
        /           \\              /              \\
      Yes          No            Yes              No
      /            \\            /                \\
    Predict      Predict     Predict          Predict
     +20          +15         +10              +5

Công thức toán học:
───────────────────

    f(X) = Σ(j=1 to J) w_j × I(X ∈ R_j)
    
    Trong đó:
    • J = số leaf nodes (terminal nodes)
    • w_j = weight của leaf j
    • R_j = region j (điều kiện để đến leaf j)
    • I(.) = indicator function (1 nếu true, 0 nếu false)

Ví dụ với tree trên:
────────────────────

    f(X) = 20 × I(is_weekend=1 AND month≥11)
         + 15 × I(is_weekend=1 AND month<11)
         + 10 × I(is_weekend=0 AND day_of_week≥5)
         + 5  × I(is_weekend=0 AND day_of_week<5)
    
    Nếu X = [is_weekend=1, month=12, day_of_week=6]:
    f(X) = 20 × 1 + 15 × 0 + 10 × 0 + 5 × 0 = 20
""")

print("""
📐 4. GRADIENT BOOSTING - TOÁN HỌC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Objective Function (Hàm mục tiêu):
───────────────────────────────────

    L = Σ(i=1 to n) l(y_i, ŷ_i) + Σ(k=1 to K) Ω(f_k)
    
    Trong đó:
    • L = Total loss (tổng loss)
    • l(y_i, ŷ_i) = loss function (MSE, MAE, etc.)
    • Ω(f_k) = regularization term (penalty cho complexity)
    • n = số samples
    • K = số trees

Loss Function (MSE cho regression):
────────────────────────────────────

    l(y, ŷ) = (y - ŷ)²
    
    VD: y = 50 (thực tế), ŷ = 48 (dự đoán)
    l = (50 - 48)² = 4

Regularization Term:
────────────────────

    Ω(f) = γT + (λ/2) Σ(j=1 to T) w_j²
    
    Trong đó:
    • T = số leaves
    • w_j = weight của leaf j
    • γ = penalty cho số leaves
    • λ = L2 regularization

Gradient Descent Update:
────────────────────────

    ŷ⁽ᵗ⁾ = ŷ⁽ᵗ⁻¹⁾ - η × ∂L/∂ŷ
    
    Trong đó:
    • ŷ⁽ᵗ⁾ = prediction ở iteration t
    • η = learning rate (thường 0.1-0.3)
    • ∂L/∂ŷ = gradient (đạo hàm)

Với MSE:
────────

    ∂L/∂ŷ = -2(y - ŷ) = -2 × residual
    
    VD: y = 50, ŷ = 48
    gradient = -2 × (50 - 48) = -4
    
    ŷ_new = 48 - 0.1 × (-4) = 48.4
""")

print("""
🔢 5. VÍ DỤ TÍNH TOÁN THỰC TẾ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scenario: Dự đoán số lượng Pasta cho ngày 15/12/2024 (Chủ nhật)
────────────────────────────────────────────────────────────────

Input Features:
───────────────

    X = {
        day_of_week: 6 (Sunday),
        day_of_month: 15,
        month: 12,
        quarter: 4,
        week_of_year: 50,
        day_of_year: 350,
        is_weekend: 1,
        day_sin: sin(2π × 350/365) = 0.95,
        day_cos: cos(2π × 350/365) = 0.31,
        month_sin: sin(2π × 12/12) = 0.0,
        month_cos: cos(2π × 12/12) = 1.0,
        is_month_start: 0,
        is_month_end: 0,
        is_quarter_start: 0,
        is_quarter_end: 0,
        is_year_start: 0,
        is_year_end: 0
    }

XGBoost Prediction Process:
────────────────────────────

    Base prediction: ŷ₀ = mean(training_data) = 50 phần
    
    Tree 1 (depth=3, 8 leaves):
    ─────────────────────────────
    • Kiểm tra: is_weekend == 1 → Go right
    • Kiểm tra: month >= 11 → Go right  
    • Kiểm tra: day_of_month >= 10 → Go right
    • Reach leaf: w₁ = +12
    
    ŷ₁ = 50 + 0.1 × 12 = 51.2  (learning_rate = 0.1)
    
    Tree 2:
    ───────
    • Learn từ residual: r₁ = y_true - ŷ₁
    • Pattern: "Sunday in December" → w₂ = +8
    
    ŷ₂ = 51.2 + 0.1 × 8 = 52.0
    
    Tree 3:
    ───────
    • Pattern: "Mid-month weekend" → w₃ = +5
    
    ŷ₃ = 52.0 + 0.1 × 5 = 52.5
    
    ...
    
    Tree 100:
    ─────────
    • Fine-tuning adjustment → w₁₀₀ = +2
    
    ŷ₁₀₀ = 71.8 + 0.1 × 2 = 72.0
    
    Final Prediction: ŷ = 72 phần

Mathematical Formula:
─────────────────────

    ŷ = ŷ₀ + η × Σ(k=1 to 100) f_k(X)
      = 50 + 0.1 × (12 + 8 + 5 + ... + 2)
      = 50 + 0.1 × 220
      = 50 + 22
      = 72 phần
""")

print("""
📊 6. SO SÁNH CÁC LOẠI REGRESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌────────────────────┬──────────────────────┬────────────────────┬──────────┐
│ Method             │ Formula Type         │ Complexity         │ Accuracy │
├────────────────────┼──────────────────────┼────────────────────┼──────────┤
│ Statistical        │ Linear               │ O(1) - instant     │ 75-80%   │
│ (μ × s × w)        │ y = ax + b           │                    │          │
├────────────────────┼──────────────────────┼────────────────────┼──────────┤
│ Linear Regression  │ Linear               │ O(n)               │ 70-75%   │
│ y = w₀ + Σw_ix_i   │ Multiple vars        │                    │          │
├────────────────────┼──────────────────────┼────────────────────┼──────────┤
│ Random Forest      │ Non-linear           │ O(n log n)         │ 85-92%   │
│ Ensemble trees     │ Piecewise constant   │                    │          │
├────────────────────┼──────────────────────┼────────────────────┼──────────┤
│ XGBoost            │ Non-linear           │ O(n log n)         │ 90-95%   │
│ Gradient boosting  │ Additive model       │                    │ 🏆       │
├────────────────────┼──────────────────────┼────────────────────┼──────────┤
│ SARIMA             │ Time series          │ O(n²)              │ 85-90%   │
│ AR + MA + Season   │ Auto-regressive      │                    │          │
└────────────────────┴──────────────────────┴────────────────────┴──────────┘

Feature Engineering:
────────────────────

    Statistical:     3 features (mean, season, weekend)
    Linear Reg:      5-7 features (manual selection)
    Random Forest:   10-15 features (automatic selection)
    XGBoost:        17 features (optimized encoding) 🏆
    SARIMA:         Time lags only (no external features)
""")

print("""
🎓 7. TẠI SAO XGBOOST TỐT HƠN?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  Non-linear Relationships:
   ──────────────────────────
   
   Statistical: y = 50 × 1.1 × 1.2 = 66 (linear)
   → Giả định mùa đông và cuối tuần NHÂN với nhau
   
   XGBoost: Học được "Sunday in December" ≠ "Saturday in December"
   → Học interactions phức tạp giữa features

2️⃣  Gradient Boosting (Học từ sai số):
   ────────────────────────────────────
   
   Tree 1: Dự đoán 50 → Sai 10
   Tree 2: Học từ sai số 10 → Fix được 8
   Tree 3: Học từ sai số 2 → Fix được 1.5
   ...
   → Mỗi tree cải thiện predictions

3️⃣  Automatic Feature Interaction:
   ─────────────────────────────────
   
   Statistical: Manual hệ số (mùa × weekend)
   XGBoost: Tự động tìm "is_weekend=1 AND month=12 AND day≥15"
   → Phát hiện patterns mà con người không nghĩ đến

4️⃣  Regularization:
   ─────────────────
   
   Ω(f) = γT + (λ/2)Σw²
   → Tránh overfitting
   → Generalize tốt cho data mới

5️⃣  Handling Missing Data:
   ───────────────────────
   
   XGBoost tự động xử lý missing values
   → Không cần imputation
   → Học được "missing-ness" cũng là feature
""")

print("""
✅ KẾT LUẬN - TRẢ LỜI CÂU HỎI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q: "Công thức dự đoán là gì?"
A: 
   Statistical: y = μ × s × w (linear multiplication)
   XGBoost:     ŷ = Σ(k=1 to K) f_k(X) (additive ensemble)

Q: "Có dùng regression không?"
A: 
   CÓ! Tất cả đều là regression (dự đoán số liên tục):
   • Statistical → Simple Linear Regression
   • XGBoost → Gradient Boosted Regression Trees
   • SARIMA → Autoregressive Time Series Regression
   • Random Forest → Ensemble Regression Trees

Q: "Regression nào tốt nhất?"
A: 
   XGBoost Gradient Boosted Regression 🏆
   • Non-linear
   • Learns from errors
   • Automatic feature interactions
   • 90-95% accuracy

📐 Công thức XGBoost đầy đủ:
────────────────────────────

    ŷ = Σ(k=1 to K) f_k(X)
    
    Với:
    • f_k(X) = Σ(j=1 to T_k) w_j,k × I(X ∈ R_j,k)
    • Minimize: L = Σ l(y_i, ŷ_i) + Σ Ω(f_k)
    • Update: ŷ⁽ᵗ⁾ = ŷ⁽ᵗ⁻¹⁾ - η × ∇L
    
    → Phức tạp nhưng chính xác nhất!
""")

print("""
🚀 DEMO THỰC TẾ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Muốn thấy XGBoost regression hoạt động?

1️⃣  Chạy comparison demo:
   $ python demo_comparison.py
   
   → Thấy rõ công thức nào chính xác hơn
   → Statistical: 830 servings (simple formula)
   → XGBoost: 747 servings (complex regression)

2️⃣  Test trên web app:
   $ streamlit run app.py
   
   → Toggle ML ON
   → Chọn XGBoost
   → Xem prediction process

3️⃣  Code implementation:
   → src/ml_forecaster.py (385 lines)
   → Xem chi tiết 17 features
   → Xem XGBoost training code

💡 Key Takeaway:
   Regression không chỉ là y = ax + b đơn giản!
   XGBoost = Advanced non-linear regression với 100+ trees! 🌲
""")
