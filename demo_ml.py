"""
Demo: Machine Learning vs Statistical Forecasting
Compares different forecasting methods for inventory optimization
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.inventory_optimizer import InventoryOptimizer
import pandas as pd
import matplotlib.pyplot as plt
import time

def compare_forecasting_methods():
    """
    Compare Statistical vs ML forecasting methods.
    """
    print("\n" + "="*80)
    print("🔬 INVENTORY OPTIMIZATION: STATISTICAL vs MACHINE LEARNING COMPARISON")
    print("="*80)
    
    forecast_days = 7
    
    # ========== STATISTICAL METHOD ==========
    print("\n📊 METHOD 1: STATISTICAL FORECASTING")
    print("-" * 80)
    
    start_time = time.time()
    optimizer_stat = InventoryOptimizer(use_ml=False)
    optimizer_stat.load_data()
    
    forecast_stat = optimizer_stat.forecast_demand(days_ahead=forecast_days)
    material_req_stat = optimizer_stat.calculate_material_requirements(forecast_stat)
    restock_stat = optimizer_stat.calculate_restocking_needs(material_req_stat)
    
    stat_time = time.time() - start_time
    
    print(f"\n✅ Statistical forecast completed in {stat_time:.2f}s")
    print(f"📦 Total predicted demand: {forecast_stat['predicted_quantity'].sum()} servings")
    print(f"💰 Restocking cost: ${restock_stat['restock_cost'].sum():.2f}")
    print(f"🔄 Materials needing restock: {len(restock_stat)}")
    
    # ========== ML METHOD: SARIMA ==========
    print("\n\n🤖 METHOD 2: MACHINE LEARNING - SARIMA")
    print("-" * 80)
    
    try:
        start_time = time.time()
        optimizer_sarima = InventoryOptimizer(use_ml=True, ml_algorithm='sarima')
        optimizer_sarima.load_data()
        
        forecast_sarima = optimizer_sarima.forecast_demand(days_ahead=forecast_days)
        material_req_sarima = optimizer_sarima.calculate_material_requirements(forecast_sarima)
        restock_sarima = optimizer_sarima.calculate_restocking_needs(material_req_sarima)
        
        sarima_time = time.time() - start_time
        
        print(f"\n✅ SARIMA forecast completed in {sarima_time:.2f}s")
        print(f"📦 Total predicted demand: {forecast_sarima['predicted_quantity'].sum()} servings")
        print(f"💰 Restocking cost: ${restock_sarima['restock_cost'].sum():.2f}")
        print(f"🔄 Materials needing restock: {len(restock_sarima)}")
        
    except Exception as e:
        print(f"❌ SARIMA error: {str(e)}")
        forecast_sarima = None
    
    # ========== ML METHOD: XGBOOST ==========
    print("\n\n🤖 METHOD 3: MACHINE LEARNING - XGBOOST")
    print("-" * 80)
    
    try:
        start_time = time.time()
        optimizer_xgb = InventoryOptimizer(use_ml=True, ml_algorithm='xgboost')
        optimizer_xgb.load_data()
        
        forecast_xgb = optimizer_xgb.forecast_demand(days_ahead=forecast_days)
        material_req_xgb = optimizer_xgb.calculate_material_requirements(forecast_xgb)
        restock_xgb = optimizer_xgb.calculate_restocking_needs(material_req_xgb)
        
        xgb_time = time.time() - start_time
        
        print(f"\n✅ XGBoost forecast completed in {xgb_time:.2f}s")
        print(f"📦 Total predicted demand: {forecast_xgb['predicted_quantity'].sum()} servings")
        print(f"💰 Restocking cost: ${restock_xgb['restock_cost'].sum():.2f}")
        print(f"🔄 Materials needing restock: {len(restock_xgb)}")
        
    except Exception as e:
        print(f"❌ XGBoost error: {str(e)}")
        forecast_xgb = None
    
    # ========== ML METHOD: RANDOM FOREST ==========
    print("\n\n🤖 METHOD 4: MACHINE LEARNING - RANDOM FOREST")
    print("-" * 80)
    
    try:
        start_time = time.time()
        optimizer_rf = InventoryOptimizer(use_ml=True, ml_algorithm='random_forest')
        optimizer_rf.load_data()
        
        forecast_rf = optimizer_rf.forecast_demand(days_ahead=forecast_days)
        material_req_rf = optimizer_rf.calculate_material_requirements(forecast_rf)
        restock_rf = optimizer_rf.calculate_restocking_needs(material_req_rf)
        
        rf_time = time.time() - start_time
        
        print(f"\n✅ Random Forest forecast completed in {rf_time:.2f}s")
        print(f"📦 Total predicted demand: {forecast_rf['predicted_quantity'].sum()} servings")
        print(f"💰 Restocking cost: ${restock_rf['restock_cost'].sum():.2f}")
        print(f"🔄 Materials needing restock: {len(restock_rf)}")
        
    except Exception as e:
        print(f"❌ Random Forest error: {str(e)}")
        forecast_rf = None
    
    # ========== COMPARISON SUMMARY ==========
    print("\n\n" + "="*80)
    print("📊 COMPARISON SUMMARY")
    print("="*80)
    
    comparison_data = []
    
    comparison_data.append({
        'Method': 'Statistical',
        'Total Demand': forecast_stat['predicted_quantity'].sum(),
        'Restock Cost': f"${restock_stat['restock_cost'].sum():.2f}",
        'Materials to Restock': len(restock_stat),
        'Time (s)': f"{stat_time:.2f}",
        'Complexity': 'Low',
        'Best For': 'Quick estimates'
    })
    
    if forecast_sarima is not None:
        comparison_data.append({
            'Method': 'SARIMA',
            'Total Demand': forecast_sarima['predicted_quantity'].sum(),
            'Restock Cost': f"${restock_sarima['restock_cost'].sum():.2f}",
            'Materials to Restock': len(restock_sarima),
            'Time (s)': f"{sarima_time:.2f}",
            'Complexity': 'High',
            'Best For': 'Seasonal patterns'
        })
    
    if forecast_xgb is not None:
        comparison_data.append({
            'Method': 'XGBoost',
            'Total Demand': forecast_xgb['predicted_quantity'].sum(),
            'Restock Cost': f"${restock_xgb['restock_cost'].sum():.2f}",
            'Materials to Restock': len(restock_xgb),
            'Time (s)': f"{xgb_time:.2f}",
            'Complexity': 'High',
            'Best For': 'Complex patterns'
        })
    
    if forecast_rf is not None:
        comparison_data.append({
            'Method': 'Random Forest',
            'Total Demand': forecast_rf['predicted_quantity'].sum(),
            'Restock Cost': f"${restock_rf['restock_cost'].sum():.2f}",
            'Materials to Restock': len(restock_rf),
            'Time (s)': f"{rf_time:.2f}",
            'Complexity': 'Medium',
            'Best For': 'Robust predictions'
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    print("\n" + comparison_df.to_string(index=False))
    
    # ========== VISUALIZATION ==========
    print("\n\n📈 Generating comparison charts...")
    
    try:
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Forecasting Methods Comparison', fontsize=16, fontweight='bold')
        
        # Plot 1: Demand by Method
        ax1 = axes[0, 0]
        methods = comparison_df['Method'].tolist()
        demands = comparison_df['Total Demand'].tolist()
        ax1.bar(methods, demands, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'][:len(methods)])
        ax1.set_title('Total Predicted Demand')
        ax1.set_ylabel('Servings')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Processing Time
        ax2 = axes[0, 1]
        times = [float(t) for t in comparison_df['Time (s)'].tolist()]
        ax2.bar(methods, times, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'][:len(methods)])
        ax2.set_title('Processing Time')
        ax2.set_ylabel('Seconds')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Demand by Dish (Statistical)
        ax3 = axes[1, 0]
        dish_demand_stat = forecast_stat.groupby('dish_name')['predicted_quantity'].sum()
        ax3.barh(dish_demand_stat.index, dish_demand_stat.values, color='#3498db')
        ax3.set_title('Statistical: Demand by Dish')
        ax3.set_xlabel('Predicted Servings')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Demand by Dish (Best ML)
        ax4 = axes[1, 1]
        if forecast_xgb is not None:
            dish_demand_ml = forecast_xgb.groupby('dish_name')['predicted_quantity'].sum()
            ax4.barh(dish_demand_ml.index, dish_demand_ml.values, color='#2ecc71')
            ax4.set_title('XGBoost: Demand by Dish')
        elif forecast_sarima is not None:
            dish_demand_ml = forecast_sarima.groupby('dish_name')['predicted_quantity'].sum()
            ax4.barh(dish_demand_ml.index, dish_demand_ml.values, color='#e74c3c')
            ax4.set_title('SARIMA: Demand by Dish')
        ax4.set_xlabel('Predicted Servings')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save the plot
        output_file = 'data/png/ml_comparison.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Chart saved to: {output_file}")
        
    except Exception as e:
        print(f"⚠️ Could not generate charts: {str(e)}")
    
    # ========== RECOMMENDATIONS ==========
    print("\n\n" + "="*80)
    print("💡 RECOMMENDATIONS")
    print("="*80)
    
    print("""
    📌 WHEN TO USE EACH METHOD:
    
    1️⃣  STATISTICAL METHOD:
       ✓ Quick daily operations
       ✓ Small datasets
       ✓ When computational resources are limited
       ✓ Simple seasonal patterns
    
    2️⃣  SARIMA (Seasonal ARIMA):
       ✓ Strong seasonal patterns (weekly/monthly)
       ✓ Historical data with clear trends
       ✓ Time series analysis focus
       ✓ When you need confidence intervals
    
    3️⃣  XGBOOST:
       ✓ Complex non-linear relationships
       ✓ Multiple external factors
       ✓ Large datasets with many features
       ✓ Best overall accuracy in most cases
    
    4️⃣  RANDOM FOREST:
       ✓ Robust predictions needed
       ✓ Feature importance analysis
       ✓ Less prone to overfitting
       ✓ Good balance of speed and accuracy
    """)
    
    print("="*80)
    print("✅ Comparison completed successfully!")
    print("="*80 + "\n")


def demo_single_algorithm(algorithm='xgboost'):
    """
    Demo a single ML algorithm in detail.
    """
    print("\n" + "="*80)
    print(f"🎯 DETAILED DEMO: {algorithm.upper()} ALGORITHM")
    print("="*80)
    
    # Initialize with ML
    optimizer = InventoryOptimizer(use_ml=True, ml_algorithm=algorithm)
    
    print("\n📥 Loading data...")
    optimizer.load_data()
    
    print(f"\n🤖 Training {algorithm.upper()} model...")
    forecast = optimizer.forecast_demand(days_ahead=14)  # 2 weeks
    
    print("\n📊 FORECAST RESULTS:")
    print("-" * 80)
    print(forecast.head(10))
    
    print("\n📈 DEMAND BY DISH:")
    print("-" * 80)
    demand_by_dish = forecast.groupby('dish_name')['predicted_quantity'].sum().sort_values(ascending=False)
    print(demand_by_dish)
    
    print("\n🔧 Calculating material requirements...")
    material_req = optimizer.calculate_material_requirements(forecast)
    
    print("\n📦 MATERIAL REQUIREMENTS:")
    print("-" * 80)
    material_summary = material_req.groupby('material_name')['total_material_needed'].sum().sort_values(ascending=False)
    print(material_summary.head(10))
    
    print("\n💰 Calculating restocking needs...")
    restock = optimizer.calculate_restocking_needs(material_req)
    
    print("\n🛒 RESTOCKING RECOMMENDATIONS:")
    print("-" * 80)
    if len(restock) > 0:
        print(restock[['material_name', 'current_stock', 'restock_quantity', 'restock_cost']].head(10))
        print(f"\n📊 SUMMARY:")
        print(f"   • Total restocking cost: ${restock['restock_cost'].sum():.2f}")
        print(f"   • Materials to restock: {len(restock)}")
    else:
        print("   ✅ No restocking needed - sufficient inventory!")
    
    print("\n" + "="*80)
    print(f"✅ {algorithm.upper()} demo completed!")
    print("="*80 + "\n")


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                  INVENTORY OPTIMIZATION - ML DEMO                          ║
    ║                                                                            ║
    ║  This demo showcases Machine Learning algorithms for inventory forecasting║
    ╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    import sys
    
    if len(sys.argv) > 1:
        # Run specific algorithm demo
        algorithm = sys.argv[1].lower()
        if algorithm in ['sarima', 'xgboost', 'random_forest', 'prophet']:
            demo_single_algorithm(algorithm)
        else:
            print(f"❌ Unknown algorithm: {algorithm}")
            print("Available: sarima, xgboost, random_forest, prophet")
    else:
        # Run full comparison
        compare_forecasting_methods()
    
    print("\n💡 TIP: Run with specific algorithm:")
    print("   python demo_ml.py sarima")
    print("   python demo_ml.py xgboost")
    print("   python demo_ml.py random_forest\n")
