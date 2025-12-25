# Dự đoán nhu cầu và tối ưu kho nguyên liệu cho nhà hàng

Hệ thống Machine Learning giúp nhà hàng dự báo chính xác nhu cầu món ăn và quản lý tồn kho hiệu quả. 

Dựa trên dataset thực tế 11,524 đơn hàng từ 2020-2025, hệ thống đạt độ chính xác 98% với XGBoost.

## Vấn đề giải quyết

Nhà hàng thường gặp khó khăn:
- Không biết ngày mai cần chuẩn bị bao nhiêu phần ăn
- Dự đoán sai → mất khách (thiếu) hoặc lãng phí (thừa)
- Nguyên liệu hết hạn gây lãng phí
- Khó tính toán chi phí và định giá hợp lý

Hệ thống này tự động hóa toàn bộ quy trình từ dự báo đến quyết định nhập hàng.

## Tính năng chính

### 1. Dự báo nhu cầu

5 thuật toán ML được so sánh: XGBoost, Random Forest, Prophet, SARIMA, Statistical

Độ chính xác:
- XGBoost: 98% (tốt nhất)
- Random Forest: 93%
- Prophet: 90%
- SARIMA: 86%
- Statistical: 78%

Hệ thống tự động điều chỉnh dự báo dựa trên:
- Thời tiết (mưa → delivery tăng 15%)
- Ngày lương (đầu tháng → chi tiêu tăng 30%)
- Sự kiện (Tết +380%, Valentine +68%)
- Cuối tuần (+45%)

### 2. Quản lý tồn kho

- Tính toán chính xác nguyên liệu cần mua
- Cảnh báo sắp hết hạn (5-7 ngày)
- Gợi ý món ăn dùng nguyên liệu sắp hỏng
- Tính tổng chi phí nhập hàng

### 3. Phân tích chi phí

- Tính COGS (Cost of Goods Sold) từng món
- Đề xuất giá bán với margin 20-50%
- Tìm món lãi/lỗ
- Xác định nguyên liệu đắt nhất

### 4. Theo dõi lãng phí

- Ghi nhận lãng phí (hết hạn, hỏng, thừa...)
- Phân tích xu hướng
- Đề xuất cải thiện
- Tính tiết kiệm tiềm năng

## Cài đặt

### Yêu cầu
- Python 3.8 trở lên
- 4GB RAM

### Setup
```bash
git clone https://github.com/RkDinhChien/Inventory_Optimization.git
cd Inventory_Optimization
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Chạy thử
```bash
# Demo nhanh (5 phút)
python scripts/demo/demo_quick.py

# So sánh các thuật toán
python scripts/demo/demo_ml.py

# Web interface
streamlit run app.py
```

## Cấu trúc project

```
Inventory_Optimization/
├── data/csv/              # Dữ liệu
│   ├── orders_real.csv           # 11,524 orders (2020-2025)
│   ├── recipes_comprehensive.csv # 161 recipes, 17 món
│   └── inventory_comprehensive.csv # 94 nguyên liệu
│
├── src/                   # Core modules
│   ├── inventory_optimizer.py    # Optimizer chính
│   ├── ml_forecaster.py          # 5 ML algorithms
│   ├── cost_analyzer.py          # Phân tích chi phí
│   ├── waste_tracker.py          # Theo dõi lãng phí
│   ├── weather_integration.py    # Tích hợp thời tiết
│   ├── market_factors.py         # Yếu tố thị trường
│   └── visualizer.py             # Biểu đồ
│
├── scripts/
│   ├── demo/              # 14 demo scripts
│   └── utils/             # 4 utility scripts
│
├── docs/                  # Documentation
│   ├── guides/            # Hướng dẫn sử dụng
│   ├── technical/         # Tài liệu kỹ thuật
│   ├── reports/           # Báo cáo, test results
│   └── reference/         # Tham khảo
│
├── app.py                 # Web app (Streamlit)
├── main.py                # CLI interface
└── requirements.txt
```

## Sử dụng

### Ví dụ cơ bản

```python
from src.inventory_optimizer import InventoryOptimizer

# Khởi tạo với XGBoost
optimizer = InventoryOptimizer(use_ml=True, ml_algorithm='xgboost')
optimizer.load_data(
    recipes_file='data/csv/recipes_comprehensive.csv',
    inventory_file='data/csv/inventory_comprehensive.csv',
    orders_file='data/csv/orders_real.csv'
)

# Dự báo 7 ngày
forecast = optimizer.forecast_demand(days_ahead=7)

# Tính nguyên liệu cần mua
materials = optimizer.calculate_material_requirements(forecast)
restocking = optimizer.calculate_restocking_needs(materials)

print(restocking)
```

### Phân tích chi phí

```python
from src.cost_analyzer import CostAnalyzer

analyzer = CostAnalyzer()
analyzer.load_data(
    'data/csv/recipes_comprehensive.csv',
    'data/csv/inventory_comprehensive.csv'
)

# Tính COGS
cogs = analyzer.calculate_cogs('Biryani_Indian')
print(f"Cost per serving: ${cogs['total_cost']:.2f}")

# Margin analysis
margin = analyzer.calculate_profit_margin('Biryani_Indian', selling_price=8.00)
print(f"Profit margin: {margin['margin_percentage']:.1f}%")
```

## Kết quả thực nghiệm

### Dataset
- 11,524 orders (2020-2025)
- 17 món ăn (Continental, Indian, Italian, Thai)
- 94 nguyên liệu (100% coverage)
- 6 năm dữ liệu lịch sử

### Model Performance

| Model | MAE | RMSE | MAPE | Accuracy |
|-------|-----|------|------|----------|
| **XGBoost** | 5.2 | 8.1 | 4.2% | **98%** |
| Random Forest | 7.1 | 11.4 | 5.8% | 93% |
| Prophet | 8.7 | 13.2 | 7.1% | 90% |
| SARIMA | 12.5 | 18.3 | 10.2% | 86% |
| Statistical | 18.3 | 25.7 | 15.5% | 78% |

XGBoost đạt accuracy cao nhất nhờ 83 features được engineer (temporal, lag, rolling, seasonal, external factors).

### Cải thiện theo giai đoạn

| Giai đoạn | Accuracy | Cải thiện |
|-----------|----------|-----------|
| Baseline (Statistical) | 78% | - |
| + ML (XGBoost) | 92% | +14% |
| + Feature Engineering | 95% | +3% |
| + External Factors | 98% | +3% |

## Documentation

### Hướng dẫn
- [Quick Start](docs/guides/QUICK_START.md) - Bắt đầu nhanh
- [Giải thích kết quả](docs/guides/GIẢI_THÍCH_KẾT_QUẢ.md) - Hiểu output hệ thống
- [ML Guide](docs/guides/ML_GUIDE.md) - Chi tiết về ML models

### Kỹ thuật
- [Mathematical Formulation](docs/technical/MATHEMATICAL_FORMULATION.md) - Công thức toán
- [System Analysis](docs/technical/SYSTEM_ANALYSIS.md) - Kiến trúc
- [Integration Guide](docs/technical/INTEGRATION_COMPLETE.md) - Tích hợp

### Báo cáo
- [System Health](docs/reports/SYSTEM_HEALTH_CHECK.md) - Tình trạng hệ thống (100/100)
- [Test Results](docs/reports/TEST_REPORT.md) - Kết quả testing
- [Dataset Evaluation](docs/reports/DATASET_EVALUATION.md) - Đánh giá dữ liệu

## Testing

Hệ thống đã pass tất cả tests:
- Core modules: 7/7 ✅
- Functionality tests: 2/2 ✅
- Data quality: 100% ✅
- System health score: 100/100 ✅

Chạy tests:
```bash
python system_check.py
```

## Tech Stack

**Core**: Python 3.9+, Pandas, NumPy

**Machine Learning**: XGBoost, Random Forest, Prophet, SARIMA (statsmodels), scikit-learn

**Web**: Streamlit, Plotly

**Visualization**: Matplotlib, Seaborn

**APIs**: OpenWeatherMap (weather data)

## License

MIT License

## Tác giả

Nguyễn Đình Chiến - Rykan

