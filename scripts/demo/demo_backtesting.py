"""
Demo: BACKTESTING - Cách đo độ chính xác thực tế
Minh họa chi tiết cách hệ thống tự test chính nó
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from src.inventory_optimizer import InventoryOptimizer

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                  BACKTESTING - ĐO ĐỘ CHÍNH XÁC THỰC TẾ                   ║
║                                                                            ║
║  Giải thích cách hệ thống tự kiểm tra độ chính xác của mình              ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

print("""
❓ CÂU HỎI: Làm sao biết model dự đoán có chính xác không?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤔 Vấn đề:
   • Chúng ta chưa biết tương lai → Không có dữ liệu thực tế để so sánh
   • Nếu dự đoán sai, khách hàng sẽ phàn nàn (quá muộn!)
   
💡 Giải pháp: BACKTESTING
   • Giả vờ "quay ngược thời gian"
   • Dùng dữ liệu cũ làm như chưa biết
   • Dự đoán "tương lai" (thực ra là quá khứ đã biết)
   • So sánh dự đoán vs thực tế
""")

print("\n" + "="*80)
print("📅 PHƯƠNG PHÁP: TRAIN-TEST SPLIT")
print("="*80 + "\n")

print("""
Ví dụ: Hôm nay là 11/12/2024, có data từ 1/1/2024 đến 10/12/2024

Bước 1: CHIA DỮ LIỆU
─────────────────────

    [============ 80% TRAINING ============][==== 20% TEST ====]
    │                                       │                   │
    1/1/2024                          1/10/2024            10/12/2024
    │                                       │                   │
    │← Dùng để học patterns                │← Giấu đi để test  │
    
    • Training set (80%): 1/1/2024 → 1/10/2024 (280 ngày)
      → Model học từ data này
      
    • Test set (20%): 2/10/2024 → 10/12/2024 (70 ngày)  
      → Giấu đi, dùng để kiểm tra

Bước 2: "QUAY LẠI QUÁ KHỨ"
───────────────────────────

    Giả sử: Hôm nay là 1/10/2024 (thay vì 11/12/2024)
    
    ┌─────────────────────────────────────────────────┐
    │ Model chỉ biết data đến 1/10/2024              │
    │ → Dự đoán 70 ngày tiếp theo (2/10 → 10/12)     │
    └─────────────────────────────────────────────────┘

Bước 3: DỰ ĐOÁN
────────────────

    Model dự đoán: "Ngày 15/10/2024 sẽ bán 50 phần Pasta"
    
    Thực tế (đã xảy ra): 15/10/2024 bán được 48 phần
    
    → Sai số: |50 - 48| = 2 phần (4%)

Bước 4: TÍNH ACCURACY
─────────────────────

    Làm với tất cả 70 ngày trong test set:
    
    ┌────────────┬──────────┬──────────┬─────────┬────────────┐
    │ Ngày       │ Thực tế  │ Dự đoán  │ Sai số  │ Sai số %   │
    ├────────────┼──────────┼──────────┼─────────┼────────────┤
    │ 02/10/2024 │    48    │    50    │    2    │    4.2%    │
    │ 03/10/2024 │    52    │    51    │    1    │    1.9%    │
    │ 04/10/2024 │    47    │    49    │    2    │    4.3%    │
    │ ...        │   ...    │   ...    │   ...   │    ...     │
    │ 10/12/2024 │    55    │    53    │    2    │    3.6%    │
    └────────────┴──────────┴──────────┴─────────┴────────────┘
    
    Accuracy = 100% - MAPE
    MAPE = Trung bình(Sai số %) = (4.2% + 1.9% + 4.3% + ... + 3.6%) / 70
    
    → Accuracy = 92.5% (MAPE = 7.5%)
""")

print("\n" + "="*80)
print("🔬 DEMO THỰC TẾ - BACKTESTING VỚI DATA THẬT")
print("="*80 + "\n")

# Load data
optimizer = InventoryOptimizer(use_ml=False)
optimizer.load_data()

orders = optimizer.orders_data.copy()
orders['date'] = pd.to_datetime(orders['date'])
orders = orders.sort_values('date')

print(f"📊 Loaded data: {len(orders)} orders")
print(f"📅 Date range: {orders['date'].min().strftime('%Y-%m-%d')} to {orders['date'].max().strftime('%Y-%m-%d')}")
print(f"📈 Total days: {(orders['date'].max() - orders['date'].min()).days} days\n")

# Split data
split_date = orders['date'].min() + timedelta(days=int(len(orders) * 0.8))
train_data = orders[orders['date'] <= split_date]
test_data = orders[orders['date'] > split_date]

print(f"🔹 TRAIN SET (80%):")
print(f"   Dates: {train_data['date'].min().strftime('%Y-%m-%d')} → {train_data['date'].max().strftime('%Y-%m-%d')}")
print(f"   Records: {len(train_data)}")
print(f"   Days: {(train_data['date'].max() - train_data['date'].min()).days}")

print(f"\n🔹 TEST SET (20%):")
print(f"   Dates: {test_data['date'].min().strftime('%Y-%m-%d')} → {test_data['date'].max().strftime('%Y-%m-%d')}")
print(f"   Records: {len(test_data)}")
print(f"   Days: {(test_data['date'].max() - test_data['date'].min()).days}")

print(f"\n{'='*80}")
print("🎬 BƯỚC 1: 'QUAY LẠI QUÁ KHỨ'")
print("="*80)

print(f"""
⏰ Giả sử: Hôm nay là {split_date.strftime('%Y-%m-%d')}
   
   • Model chỉ biết data đến ngày này
   • Cần dự đoán {(test_data['date'].max() - split_date).days} ngày tiếp theo
   • Thực ra chúng ta đã có data thực tế (để so sánh)
""")

print(f"\n{'='*80}")
print("🔮 BƯỚC 2: DỰ ĐOÁN")
print("="*80)

# Retrain với train data only
optimizer.orders_data = train_data
days_to_predict = (test_data['date'].max() - split_date).days

print(f"\n⚙️  Training model với {len(train_data)} records...")
print(f"📊 Generating forecast for {days_to_predict} days...\n")

try:
    forecast = optimizer.forecast_demand(days_ahead=days_to_predict)
    
    print(f"✅ Forecast generated: {len(forecast)} predictions")
    
    # Prepare comparison
    forecast['date'] = pd.to_datetime(forecast['date'])
    test_aggregated = test_data.groupby(['date', 'dish_name'])['quantity_sold'].sum().reset_index()
    
    # Merge
    comparison = test_aggregated.merge(
        forecast[['date', 'dish_name', 'predicted_quantity']],
        on=['date', 'dish_name'],
        how='inner'
    )
    
    if len(comparison) == 0:
        print("⚠️  No overlapping data for comparison")
    else:
        print(f"✅ Found {len(comparison)} matching data points for comparison")
        
        print(f"\n{'='*80}")
        print("📊 BƯỚC 3: SO SÁNH VỚI THỰC TẾ")
        print("="*80)
        
        # Calculate errors
        comparison['error'] = abs(comparison['quantity_sold'] - comparison['predicted_quantity'])
        comparison['error_pct'] = (comparison['error'] / comparison['quantity_sold'] * 100)
        
        # Sample predictions
        print(f"\n📝 SAMPLE: 10 dự đoán đầu tiên")
        print("-"*80)
        print(f"{'Date':<12} {'Dish':<20} {'Actual':>8} {'Predict':>8} {'Error':>8} {'Error%':>8}")
        print("-"*80)
        
        for idx, row in comparison.head(10).iterrows():
            date_str = row['date'].strftime('%Y-%m-%d')
            dish_short = row['dish_name'][:18]
            print(f"{date_str:<12} {dish_short:<20} "
                  f"{row['quantity_sold']:>8.0f} "
                  f"{row['predicted_quantity']:>8.0f} "
                  f"{row['error']:>8.0f} "
                  f"{row['error_pct']:>7.1f}%")
        
        print(f"\n{'='*80}")
        print("📈 BƯỚC 4: TÍNH ACCURACY")
        print("="*80)
        
        # Calculate metrics
        mae = comparison['error'].mean()
        rmse = np.sqrt((comparison['error'] ** 2).mean())
        mape = comparison['error_pct'].mean()
        accuracy = 100 - mape
        
        print(f"""
🎯 KẾT QUẢ BACKTESTING:
─────────────────────────────────────────────────────────────────────────────

  📊 Tổng số dự đoán:              {len(comparison):>10}
  
  📏 MAE (Mean Absolute Error):    {mae:>10.2f} units
     → Trung bình sai lệch {mae:.1f} đơn vị
  
  📐 RMSE (Root Mean Sq Error):    {rmse:>10.2f} units
     → Phạt nặng những dự đoán sai xa
  
  📊 MAPE (Mean Abs % Error):      {mape:>10.2f}%
     → Trung bình sai {mape:.1f}%
  
  ✅ ACCURACY:                     {accuracy:>10.2f}%
     → Dự đoán đúng {accuracy:.1f}%

─────────────────────────────────────────────────────────────────────────────

💡 Đánh giá:
  {f'🏆 Xuất sắc! (>90%)' if accuracy > 90 else 
   f'✅ Tốt! (85-90%)' if accuracy > 85 else
   f'⚠️  Chấp nhận được (75-85%)' if accuracy > 75 else
   f'❌ Cần cải thiện (<75%)'}
  
  Với accuracy {accuracy:.1f}%, hệ thống:
  {'✓ Đáng tin cậy cho quyết định kinh doanh quan trọng' if accuracy > 85 else
   '⚠️  Nên dùng thêm judgement của con người'}
  {'✓ Có thể tự động hóa hoàn toàn' if accuracy > 90 else
   '⚠️  Cần monitoring thường xuyên'}
""")
        
        # Distribution analysis
        print(f"\n{'='*80}")
        print("📊 PHÂN TÍCH PHÂN BỐ SAI SỐ")
        print("="*80 + "\n")
        
        excellent = len(comparison[comparison['error_pct'] < 5])
        good = len(comparison[(comparison['error_pct'] >= 5) & (comparison['error_pct'] < 10)])
        acceptable = len(comparison[(comparison['error_pct'] >= 10) & (comparison['error_pct'] < 20)])
        poor = len(comparison[comparison['error_pct'] >= 20])
        
        total = len(comparison)
        
        print(f"  🟢 Xuất sắc (<5% error):      {excellent:>5} ({excellent/total*100:>5.1f}%)  {'█' * int(excellent/total*50)}")
        print(f"  🟡 Tốt (5-10% error):         {good:>5} ({good/total*100:>5.1f}%)  {'█' * int(good/total*50)}")
        print(f"  🟠 Chấp nhận (10-20% error):  {acceptable:>5} ({acceptable/total*100:>5.1f}%)  {'█' * int(acceptable/total*50)}")
        print(f"  🔴 Cần cải thiện (>20% error): {poor:>5} ({poor/total*100:>5.1f}%)  {'█' * int(poor/total*50)}")

except Exception as e:
    print(f"\n❌ Error during backtesting: {e}")
    import traceback
    traceback.print_exc()

print(f"\n\n{'='*80}")
print("🎓 TÓM TẮT: BACKTESTING LÀ GÌ?")
print("="*80)

print("""
Backtesting = Kiểm tra độ chính xác bằng cách "quay lại quá khứ"

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  KHÔNG BACKTESTING (Nguy hiểm):                                        │
│  ─────────────────────────────                                         │
│  ❌ Dự đoán → Áp dụng → Chờ → Phát hiện sai → Quá muộn!               │
│                                                                         │
│  CÓ BACKTESTING (An toàn):                                             │
│  ───────────────────────                                               │
│  ✅ Chia data → Train → Test với data cũ → Đo accuracy → Tin tưởng    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

🔑 Key Points:
──────────────

1. Data split: 80% train, 20% test
   → Đủ data để học, đủ data để test

2. Temporal order: Test set luôn sau train set
   → Giống thực tế: dự đoán tương lai chứ không quay lại quá khứ

3. No data leakage: Model không biết test set khi training
   → Đảm bảo đánh giá trung thực

4. Multiple metrics: MAE, RMSE, MAPE, Accuracy
   → Hiểu toàn diện về performance

5. Continuous validation: Chạy lại mỗi khi có data mới
   → Đảm bảo model vẫn chính xác theo thời gian

💡 Câu trả lời cho câu hỏi:
───────────────────────────

"Độ chính xác dựa trên gì?"
→ Dựa trên việc so sánh dự đoán với thực tế trong quá khứ

"Có phải giả sử lùi lại vài ngày?"
→ ĐÚNG! Lùi lại 20% timeline, giả vờ chưa biết, rồi dự đoán

"Rồi dự đoán sau đó so sánh với hiện tại?"
→ ĐÚNG! So sánh dự đoán với data thực tế đã xảy ra

"Hay làm như nào?"
→ Chính xác là phương pháp Train-Test Split + Backtesting như demo trên!
""")

print(f"\n{'='*80}")
print("🚀 BƯỚC TIẾP THEO")
print("="*80)

print("""
Giờ bạn đã hiểu backtesting! Hãy:

1️⃣  So sánh Statistical vs XGBoost:
   $ python demo_comparison.py
   → Xem XGBoost có accuracy cao hơn bao nhiêu

2️⃣  Test trên web app:
   $ streamlit run app.py
   → Toggle ML, run analysis, xem kết quả

3️⃣  Với data thực (119M orders):
   → Backtesting sẽ chính xác hơn nhiều
   → Vì model có nhiều data để học patterns

💡 Remember: 
   Accuracy >85% = Đủ tin cậy để tự động hóa quyết định kinh doanh!
""")
