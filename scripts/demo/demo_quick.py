"""
Quick Demo - Statistical Forecasting (No ML Required)
Demonstrates the inventory optimization system without ML dependencies
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║           INVENTORY OPTIMIZATION DEMO - STATISTICAL METHOD                 ║
║                                                                            ║
║  This demo works WITHOUT ML libraries - perfect for quick testing!        ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.inventory_optimizer import InventoryOptimizer
    import pandas as pd
    
    print("\n📥 Initializing Inventory Optimizer (Statistical Mode)...")
    optimizer = InventoryOptimizer(use_ml=False)
    
    print("📊 Loading sample data...")
    optimizer.load_data()
    
    print(f"   • Historical orders: {len(optimizer.orders_data)} records")
    print(f"   • Current inventory: {len(optimizer.inventory_data)} items")
    print(f"   • Recipe database: {len(optimizer.recipes_data)} entries")
    
    # 7-day forecast
    print("\n" + "="*80)
    print("📈 DEMAND FORECAST (Next 7 Days)")
    print("="*80)
    
    forecast = optimizer.forecast_demand(days_ahead=7)
    
    print(f"\n✅ Forecast generated: {len(forecast)} predictions")
    print(f"📊 Total predicted demand: {forecast['predicted_quantity'].sum()} servings")
    
    # Demand by dish
    print("\n🍽️  PREDICTED DEMAND BY DISH:")
    print("-" * 80)
    demand_by_dish = forecast.groupby('dish_name')['predicted_quantity'].sum().sort_values(ascending=False)
    for dish, quantity in demand_by_dish.items():
        print(f"   {dish:.<40} {int(quantity):>4} servings")
    
    # Material requirements
    print("\n" + "="*80)
    print("📦 MATERIAL REQUIREMENTS")
    print("="*80)
    
    material_req = optimizer.calculate_material_requirements(forecast)
    material_summary = material_req.groupby('material_name')['total_material_needed'].sum().sort_values(ascending=False)
    
    print(f"\n✅ {len(material_summary)} materials needed")
    print("\n🔝 TOP 10 MATERIALS:")
    print("-" * 80)
    for material, quantity in material_summary.head(10).items():
        print(f"   {material:.<40} {quantity:>7.2f} units")
    
    # Restocking needs
    print("\n" + "="*80)
    print("🔄 RESTOCKING RECOMMENDATIONS")
    print("="*80)
    
    restock = optimizer.calculate_restocking_needs(material_req)
    
    if len(restock) > 0:
        print(f"\n⚠️  {len(restock)} materials need restocking")
        print(f"💰 Total investment required: ${restock['restock_cost'].sum():.2f}")
        
        print("\n📋 URGENT RESTOCKING LIST:")
        print("-" * 80)
        print(f"{'Material':<30} {'Current':>10} {'Needed':>10} {'Cost':>12}")
        print("-" * 80)
        
        for idx, row in restock.head(10).iterrows():
            print(f"{row['material_name']:<30} "
                  f"{row['current_stock']:>10.1f} "
                  f"{row['restock_quantity']:>10.1f} "
                  f"${row['restock_cost']:>11.2f}")
    else:
        print("\n✅ All materials are sufficiently stocked!")
    
    # Near expiry materials
    print("\n" + "="*80)
    print("⏰ NEAR-EXPIRY MATERIALS")
    print("="*80)
    
    near_expiry = optimizer.find_near_expiry_materials(days_threshold=5)
    
    if len(near_expiry) > 0:
        print(f"\n⚠️  {len(near_expiry)} materials expiring within 5 days")
        
        print("\n🚨 URGENT - USE THESE MATERIALS FIRST:")
        print("-" * 80)
        print(f"{'Material':<30} {'Stock':>10} {'Days Left':>12} {'Expiry Date':>15}")
        print("-" * 80)
        
        for idx, row in near_expiry.iterrows():
            expiry_date = pd.to_datetime(row['expiry_date']).strftime('%Y-%m-%d')
            print(f"{row['material_name']:<30} "
                  f"{row['current_stock']:>10.1f} "
                  f"{row['days_until_expiry']:>12.0f} "
                  f"{expiry_date:>15}")
    else:
        print("\n✅ No materials expiring soon - good inventory management!")
    
    # Dish recommendations
    print("\n" + "="*80)
    print("💡 DISH RECOMMENDATIONS")
    print("="*80)
    
    recommendations = optimizer.recommend_dishes(max_recommendations=5)
    
    if len(recommendations) > 0:
        print(f"\n💡 {len(recommendations)} dishes can help use near-expiry materials")
        
        print("\n🍽️  SUGGESTED DISHES TO PREPARE:")
        print("-" * 80)
        print(f"{'Dish Name':<35} {'Max Servings':>15} {'Score':>15}")
        print("-" * 80)
        
        for idx, row in recommendations.head(10).iterrows():
            print(f"{row['dish_name']:<35} "
                  f"{row['max_servings_possible']:>15.0f} "
                  f"{row['recommendation_score']:>15.2f}")
    else:
        print("\n✅ No urgent dish recommendations needed")
    
    # Summary
    print("\n" + "="*80)
    print("📊 OPTIMIZATION SUMMARY")
    print("="*80)
    
    print(f"""
    📈 Forecast Period:              7 days
    🍽️  Total Predicted Servings:    {forecast['predicted_quantity'].sum()}
    📦 Materials Required:           {len(material_summary)}
    🔄 Materials to Restock:         {len(restock)}
    💰 Restocking Investment:        ${restock['restock_cost'].sum() if len(restock) > 0 else 0:.2f}
    ⏰ Materials Expiring Soon:      {len(near_expiry)}
    💡 Dish Recommendations:         {len(recommendations)}
    """)
    
    print("="*80)
    print("✅ DEMO COMPLETED SUCCESSFULLY!")
    print("="*80)
    
    print("""
    🎯 WHAT'S NEXT?
    
    1️⃣  Upgrade to ML Forecasting:
       • Install dependencies: ./setup.sh
       • Try ML demo: python3 demo_ml.py
       • Compare algorithms: python3 demo_ml.py xgboost
    
    2️⃣  Explore More Features:
       • Full system: python3 main.py
       • Examples: python3 examples.py
       • Visualizations: Check data/png/ folder
    
    3️⃣  Read Documentation:
       • README.md - Project overview
       • ML_GUIDE.md - ML algorithms details
    
    💡 TIP: This statistical method is fast and reliable for daily use!
        ML methods provide higher accuracy for complex patterns.
    """)

except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\n💡 Make sure you have pandas and numpy installed:")
    print("   pip3 install pandas numpy matplotlib")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print("\n💡 If you see Xcode errors, run: xcode-select --install")
