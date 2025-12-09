"""
Simple Test - Statistical Forecasting Only
Tests the system without ML dependencies
"""

print("\n" + "="*80)
print("🧪 TESTING INVENTORY OPTIMIZATION SYSTEM (Statistical Mode)")
print("="*80)

# Test 1: Basic imports
print("\n1️⃣  Testing basic imports...")
try:
    import sys
    import os
    import pandas as pd
    import numpy as np
    print("   ✅ pandas, numpy - OK")
except Exception as e:
    print(f"   ❌ Import error: {str(e)}")
    sys.exit(1)

# Test 2: Import optimizer
print("\n2️⃣  Testing InventoryOptimizer import...")
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from src.inventory_optimizer import InventoryOptimizer
    print("   ✅ InventoryOptimizer imported successfully")
except Exception as e:
    print(f"   ❌ Failed to import: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Create optimizer instance
print("\n3️⃣  Creating optimizer instance...")
try:
    optimizer = InventoryOptimizer(use_ml=False)
    print("   ✅ Optimizer created (Statistical mode)")
except Exception as e:
    print(f"   ❌ Failed to create: {str(e)}")
    sys.exit(1)

# Test 4: Load data
print("\n4️⃣  Loading sample data...")
try:
    optimizer.load_data()
    print(f"   ✅ Data loaded successfully")
    print(f"   📊 Orders: {len(optimizer.orders_data)} rows")
    print(f"   📦 Inventory: {len(optimizer.inventory_data)} items")
    print(f"   📝 Recipes: {len(optimizer.recipes_data)} entries")
except Exception as e:
    print(f"   ❌ Failed to load data: {str(e)}")
    sys.exit(1)

# Test 5: Forecast demand
print("\n5️⃣  Testing demand forecasting (3 days)...")
try:
    forecast = optimizer.forecast_demand(days_ahead=3)
    print(f"   ✅ Forecast generated: {len(forecast)} predictions")
    print(f"   📊 Total predicted demand: {forecast['predicted_quantity'].sum()} servings")
    print(f"   🍽️  Dishes forecasted: {forecast['dish_name'].nunique()}")
except Exception as e:
    print(f"   ❌ Forecast failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Calculate material requirements
print("\n6️⃣  Calculating material requirements...")
try:
    material_req = optimizer.calculate_material_requirements(forecast)
    print(f"   ✅ Material requirements calculated")
    print(f"   📦 Materials needed: {material_req['material_name'].nunique()}")
    print(f"   🔢 Total entries: {len(material_req)}")
except Exception as e:
    print(f"   ❌ Material calculation failed: {str(e)}")
    sys.exit(1)

# Test 7: Calculate restocking needs
print("\n7️⃣  Calculating restocking needs...")
try:
    restock = optimizer.calculate_restocking_needs(material_req)
    print(f"   ✅ Restocking analysis completed")
    print(f"   🔄 Materials needing restock: {len(restock)}")
    if len(restock) > 0:
        print(f"   💰 Total restocking cost: ${restock['restock_cost'].sum():.2f}")
        print(f"\n   Top 3 expensive restocks:")
        for idx, row in restock.head(3).iterrows():
            print(f"      • {row['material_name']}: {row['restock_quantity']:.2f} units (${row['restock_cost']:.2f})")
    else:
        print("   ℹ️  No restocking needed at this time")
except Exception as e:
    print(f"   ❌ Restocking calculation failed: {str(e)}")
    sys.exit(1)

# Test 8: Near expiry materials
print("\n8️⃣  Finding near-expiry materials...")
try:
    near_expiry = optimizer.find_near_expiry_materials(days_threshold=5)
    print(f"   ✅ Near-expiry analysis completed")
    print(f"   ⚠️  Materials expiring soon: {len(near_expiry)}")
    if len(near_expiry) > 0:
        print(f"\n   Materials to use urgently:")
        for idx, row in near_expiry.head(3).iterrows():
            print(f"      • {row['material_name']}: {row['days_until_expiry']} days left")
except Exception as e:
    print(f"   ❌ Near-expiry check failed: {str(e)}")
    sys.exit(1)

# Test 9: Dish recommendations
print("\n9️⃣  Getting dish recommendations...")
try:
    recommendations = optimizer.recommend_dishes_for_near_expiry(days_threshold=5)
    print(f"   ✅ Recommendations generated")
    print(f"   🍽️  Suggested dishes: {len(recommendations)}")
    if len(recommendations) > 0:
        print(f"\n   Top recommendations:")
        for idx, row in recommendations.head(3).iterrows():
            print(f"      • {row['dish_name']}: {row['max_servings']:.0f} servings possible")
except Exception as e:
    print(f"   ❌ Recommendations failed: {str(e)}")
    sys.exit(1)

# Summary
print("\n" + "="*80)
print("✅ ALL TESTS PASSED!")
print("="*80)

print("""
📊 SYSTEM STATUS:
   ✓ Core functionality: Working
   ✓ Statistical forecasting: Working
   ✓ Material calculations: Working
   ✓ Restocking analysis: Working
   ✓ Near-expiry tracking: Working
   ✓ Dish recommendations: Working

🎯 NEXT STEPS:
   1. Run the main system: python3 main.py
   2. Try the examples: python3 examples.py
   3. For ML features, install required libraries:
      - Install Xcode Command Line Tools first (macOS)
      - Then: pip3 install statsmodels xgboost prophet

📝 NOTE:
   ML algorithms are optional. The system works perfectly with
   statistical methods for quick and reliable forecasting!
""")

print("="*80 + "\n")
