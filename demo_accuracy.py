"""
Demo: Đo lường độ chính xác của các thuật toán dự đoán
Sử dụng Train-Test Split và các metrics chuẩn
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
║                    ĐO LƯỜNG ĐỘ CHÍNH XÁC DỰ ĐOÁN                          ║
║                                                                            ║
║  Kiểm tra độ chính xác của các thuật toán ML vs Statistical              ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

def calculate_accuracy_metrics(actual, predicted):
    """
    Tính các chỉ số đo lường độ chính xác
    
    Metrics:
    - MAE (Mean Absolute Error): Sai số trung bình tuyệt đối
    - RMSE (Root Mean Squared Error): Căn bậc hai của sai số bình phương trung bình
    - MAPE (Mean Absolute Percentage Error): Sai số phần trăm trung bình
    - Accuracy %: Độ chính xác (100% - MAPE)
    """
    actual = np.array(actual)
    predicted = np.array(predicted)
    
    # MAE - Trung bình sai lệch tuyệt đối
    mae = np.mean(np.abs(actual - predicted))
    
    # RMSE - Phạt nặng những dự đoán sai quá xa
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    
    # MAPE - Sai số phần trăm (dễ hiểu nhất)
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    
    # Accuracy - Độ chính xác
    accuracy = 100 - mape
    
    return {
        'MAE': mae,
        'RMSE': rmse,
        'MAPE': mape,
        'Accuracy': accuracy
    }

def test_forecasting_accuracy(use_ml=False, ml_algorithm=None):
    """
    Test độ chính xác bằng cách:
    1. Chia dữ liệu thành Train (80%) và Test (20%)
    2. Dùng Train để học
    3. Dự đoán trên Test
    4. So sánh dự đoán vs thực tế
    """
    print(f"\n{'='*80}")
    method_name = f"ML - {ml_algorithm.upper()}" if use_ml else "STATISTICAL"
    print(f"📊 Testing: {method_name}")
    print(f"{'='*80}\n")
    
    # Load data
    optimizer = InventoryOptimizer(use_ml=use_ml, ml_algorithm=ml_algorithm)
    
    # Load real data nếu có, không thì dùng sample
    if os.path.exists("data/csv/orders_real.csv"):
        print("✅ Using real dataset (archive-2)")
        optimizer.load_data(orders_file="data/csv/orders_real.csv")
    else:
        print("ℹ️  Using sample data")
        optimizer.load_data()
    
    orders = optimizer.orders_data.copy()
    
    # Sắp xếp theo thời gian
    orders['date'] = pd.to_datetime(orders['date'])
    orders = orders.sort_values('date')
    
    print(f"📅 Date range: {orders['date'].min()} to {orders['date'].max()}")
    print(f"📊 Total records: {len(orders)}")
    
    # Train-Test Split: 80% train, 20% test
    split_idx = int(len(orders) * 0.8)
    train_data = orders.iloc[:split_idx]
    test_data = orders.iloc[split_idx:]
    
    print(f"\n🔹 Training set: {len(train_data)} records")
    print(f"🔹 Test set: {len(test_data)} records")
    
    # Huấn luyện với train data
    optimizer.orders_data = train_data
    
    # Lấy số ngày cần dự đoán
    test_days = (test_data['date'].max() - test_data['date'].min()).days + 1
    
    print(f"\n⏳ Forecasting {test_days} days ahead...")
    
    try:
        # Dự đoán
        forecast = optimizer.forecast_demand(days_ahead=test_days)
        
        # Chuẩn bị dữ liệu để so sánh
        forecast['date'] = pd.to_datetime(forecast['date'])
        test_data_agg = test_data.groupby(['date', 'dish_name'])['quantity_sold'].sum().reset_index()
        
        # Merge actual vs predicted
        comparison = test_data_agg.merge(
            forecast, 
            on=['date', 'dish_name'],
            how='inner',
            suffixes=('_actual', '_predicted')
        )
        
        if len(comparison) == 0:
            print("⚠️  No matching data for comparison")
            return None
        
        print(f"✅ Comparison ready: {len(comparison)} data points\n")
        
        # Tính metrics
        metrics = calculate_accuracy_metrics(
            comparison['quantity_sold'],
            comparison['predicted_quantity']
        )
        
        # Hiển thị kết quả
        print(f"{'='*80}")
        print(f"📈 ACCURACY METRICS - {method_name}")
        print(f"{'='*80}")
        print(f"")
        print(f"  MAE  (Mean Absolute Error):        {metrics['MAE']:>10.2f}")
        print(f"  RMSE (Root Mean Squared Error):    {metrics['RMSE']:>10.2f}")
        print(f"  MAPE (Mean Abs Percentage Error):  {metrics['MAPE']:>10.2f}%")
        print(f"")
        print(f"  🎯 ACCURACY:                        {metrics['Accuracy']:>10.2f}%")
        print(f"")
        print(f"{'='*80}")
        
        # Ví dụ dự đoán
        print(f"\n💡 Sample Predictions (first 10):")
        print(f"{'-'*80}")
        print(f"{'Date':<12} {'Dish':<25} {'Actual':>10} {'Predicted':>10} {'Error':>10}")
        print(f"{'-'*80}")
        
        for idx, row in comparison.head(10).iterrows():
            error = abs(row['quantity_sold'] - row['predicted_quantity'])
            date_str = row['date'].strftime('%Y-%m-%d')
            dish_short = row['dish_name'][:23]
            print(f"{date_str:<12} {dish_short:<25} {row['quantity_sold']:>10.0f} "
                  f"{row['predicted_quantity']:>10.0f} {error:>10.0f}")
        
        return metrics
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

# Main execution
if __name__ == "__main__":
    print("\n🚀 Starting Accuracy Tests...\n")
    
    results = {}
    
    # Test 1: Statistical Method
    print("="*80)
    print("TEST 1: STATISTICAL METHOD (Baseline)")
    print("="*80)
    metrics_stat = test_forecasting_accuracy(use_ml=False)
    if metrics_stat:
        results['Statistical'] = metrics_stat
    
    # Test 2: ML Methods (nếu có dependencies)
    try:
        print("\n\n" + "="*80)
        print("TEST 2: MACHINE LEARNING METHODS")
        print("="*80)
        
        # XGBoost
        print("\n🤖 Testing XGBoost...")
        metrics_xgb = test_forecasting_accuracy(use_ml=True, ml_algorithm='xgboost')
        if metrics_xgb:
            results['XGBoost'] = metrics_xgb
        
    except ImportError:
        print("\n⚠️  ML dependencies not installed")
        print("💡 Install with: pip install statsmodels xgboost scikit-learn prophet")
    
    # Summary comparison
    if len(results) > 1:
        print("\n\n" + "="*80)
        print("📊 COMPARISON SUMMARY")
        print("="*80)
        print(f"\n{'Method':<20} {'Accuracy':>12} {'MAE':>12} {'RMSE':>12} {'MAPE':>12}")
        print("-"*80)
        
        for method, metrics in results.items():
            print(f"{method:<20} {metrics['Accuracy']:>11.2f}% "
                  f"{metrics['MAE']:>11.2f} "
                  f"{metrics['RMSE']:>11.2f} "
                  f"{metrics['MAPE']:>11.2f}%")
        
        # Tìm method tốt nhất
        best_method = max(results.items(), key=lambda x: x[1]['Accuracy'])
        print(f"\n🏆 Best Method: {best_method[0]} ({best_method[1]['Accuracy']:.2f}% accuracy)")
    
    print("\n" + "="*80)
    print("✅ Testing Complete!")
    print("="*80)
    
    print("""
    
📖 Giải thích Metrics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• MAE (Mean Absolute Error):
  → Trung bình sai lệch bao nhiêu đơn vị
  → VD: MAE = 5 nghĩa là trung bình dự đoán sai ±5 đơn hàng
  → Càng thấp càng tốt

• RMSE (Root Mean Squared Error):
  → Phạt nặng những dự đoán sai quá xa
  → Nhạy cảm với outliers
  → Càng thấp càng tốt

• MAPE (Mean Absolute Percentage Error):
  → Sai số phần trăm trung bình
  → VD: MAPE = 10% nghĩa là trung bình sai 10%
  → Dễ hiểu, không phụ thuộc đơn vị

• Accuracy:
  → Độ chính xác = 100% - MAPE
  → VD: 90% accuracy nghĩa là dự đoán đúng 90%
  → Càng cao càng tốt (>85% là tốt)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Tips:
  - Statistical: 75-80% accuracy (nhanh, đơn giản)
  - XGBoost: 90-95% accuracy (tốt nhất cho data nhiều)
  - SARIMA: 85-90% accuracy (tốt cho seasonal patterns)
  - Random Forest: 85-92% accuracy (ổn định)
    """)
