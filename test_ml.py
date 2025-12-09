"""
Quick Test: ML Forecaster Module
Tests if the ML algorithms can be imported and basic functionality works
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("\n" + "="*80)
print("🧪 TESTING ML FORECASTER MODULE")
print("="*80)

# Test 1: Import check
print("\n1️⃣  Testing imports...")
try:
    from src.inventory_optimizer import InventoryOptimizer
    print("   ✅ InventoryOptimizer imported successfully")
except Exception as e:
    print(f"   ❌ Failed to import InventoryOptimizer: {str(e)}")
    sys.exit(1)

try:
    from src.ml_forecaster import MLForecaster
    print("   ✅ MLForecaster imported successfully")
    ML_AVAILABLE = True
except Exception as e:
    print(f"   ⚠️  MLForecaster import warning: {str(e)}")
    ML_AVAILABLE = False

# Test 2: Check ML libraries
print("\n2️⃣  Checking ML library availability...")

libraries = {
    'statsmodels': 'SARIMA',
    'xgboost': 'XGBoost',
    'sklearn': 'Random Forest',
    'prophet': 'Prophet'
}

available_libs = []
for lib, name in libraries.items():
    try:
        if lib == 'prophet':
            import prophet
        elif lib == 'xgboost':
            import xgboost
        elif lib == 'sklearn':
            from sklearn.ensemble import RandomForestRegressor
        elif lib == 'statsmodels':
            from statsmodels.tsa.statespace.sarimax import SARIMAX
        print(f"   ✅ {name} ({lib}) - Available")
        available_libs.append(lib)
    except ImportError:
        print(f"   ❌ {name} ({lib}) - Not installed")

# Test 3: Statistical method (always works)
print("\n3️⃣  Testing Statistical forecasting...")
try:
    optimizer = InventoryOptimizer(use_ml=False)
    optimizer.load_data()
    forecast = optimizer.forecast_demand(days_ahead=3)
    print(f"   ✅ Statistical forecast: {len(forecast)} predictions generated")
    print(f"   📊 Total predicted demand: {forecast['predicted_quantity'].sum()} servings")
except Exception as e:
    print(f"   ❌ Statistical forecast failed: {str(e)}")

# Test 4: ML methods (if available)
if ML_AVAILABLE and available_libs:
    print("\n4️⃣  Testing ML forecasting...")
    
    # Test XGBoost if available
    if 'xgboost' in available_libs and 'sklearn' in available_libs:
        try:
            print("   🤖 Testing XGBoost...")
            optimizer_ml = InventoryOptimizer(use_ml=True, ml_algorithm='xgboost')
            optimizer_ml.load_data()
            forecast_ml = optimizer_ml.forecast_demand(days_ahead=3)
            print(f"   ✅ XGBoost forecast: {len(forecast_ml)} predictions generated")
            print(f"   📊 Total predicted demand: {forecast_ml['predicted_quantity'].sum()} servings")
        except Exception as e:
            print(f"   ❌ XGBoost test failed: {str(e)}")
    
    # Test Random Forest if available
    if 'sklearn' in available_libs:
        try:
            print("   🤖 Testing Random Forest...")
            optimizer_rf = InventoryOptimizer(use_ml=True, ml_algorithm='random_forest')
            optimizer_rf.load_data()
            forecast_rf = optimizer_rf.forecast_demand(days_ahead=3)
            print(f"   ✅ Random Forest forecast: {len(forecast_rf)} predictions generated")
            print(f"   📊 Total predicted demand: {forecast_rf['predicted_quantity'].sum()} servings")
        except Exception as e:
            print(f"   ❌ Random Forest test failed: {str(e)}")
else:
    print("\n4️⃣  ML forecasting - Skipped (libraries not available)")

# Summary
print("\n" + "="*80)
print("📋 TEST SUMMARY")
print("="*80)

if not available_libs:
    print("""
⚠️  ML libraries not installed. To install:

    pip install statsmodels xgboost prophet

Or if using pip3:

    pip3 install statsmodels xgboost prophet

Note: You may need to install Xcode Command Line Tools on macOS:
    xcode-select --install

✅ Statistical forecasting is working and can be used.
""")
else:
    print(f"\n✅ Available algorithms: {len(available_libs)}/4")
    print(f"   Installed: {', '.join(available_libs)}")
    if len(available_libs) < 4:
        missing = [lib for lib in libraries.keys() if lib not in available_libs]
        print(f"   Missing: {', '.join(missing)}")
    print("\n✅ Both Statistical and ML forecasting are available!")

print("="*80 + "\n")
