#!/usr/bin/env python3
"""
COMPREHENSIVE SYSTEM CHECK
Tests all components and generates health report
"""

import sys
import os
sys.path.insert(0, 'src')

import pandas as pd
from datetime import datetime

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def main():
    print("\n🔍 INVENTORY OPTIMIZATION SYSTEM - COMPREHENSIVE CHECK")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    score = 100  # Start with perfect score
    issues = []
    
    # ============================================================
    # 1. PYTHON ENVIRONMENT
    # ============================================================
    print_section("1. PYTHON ENVIRONMENT")
    print(f"✅ Python version: {sys.version.split()[0]}")
    print(f"✅ Python path: {sys.executable}")
    
    # ============================================================
    # 2. CORE MODULES
    # ============================================================
    print_section("2. CORE MODULES")
    
    modules_status = {}
    modules = [
        'inventory_optimizer',
        'ml_forecaster',
        'cost_analyzer',
        'waste_tracker',
        'weather_integration',
        'market_factors',
        'visualizer'
    ]
    
    for mod in modules:
        try:
            __import__(mod)
            modules_status[mod] = "✅ OK"
            print(f"✅ {mod}")
        except Exception as e:
            modules_status[mod] = f"❌ {str(e)[:50]}"
            print(f"❌ {mod}: {str(e)[:50]}")
            score -= 10
            issues.append(f"Module {mod} failed: {str(e)[:50]}")
    
    # ============================================================
    # 3. DATASETS
    # ============================================================
    print_section("3. DATASETS")
    
    datasets = {
        'recipes': 'data/csv/recipes_comprehensive.csv',
        'inventory': 'data/csv/inventory_comprehensive.csv',
        'orders': 'data/csv/orders_real.csv'
    }
    
    data = {}
    for name, path in datasets.items():
        try:
            df = pd.read_csv(path)
            data[name] = df
            print(f"✅ {name}: {len(df):,} rows")
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
            score -= 15
            issues.append(f"Dataset {name} failed to load")
    
    # ============================================================
    # 4. DATA QUALITY
    # ============================================================
    print_section("4. DATA QUALITY")
    
    if 'orders' in data:
        orders = data['orders']
        orders['date'] = pd.to_datetime(orders['date'])
        
        print(f"📊 Orders: {len(orders):,}")
        print(f"📅 Date range: {orders['date'].min().date()} to {orders['date'].max().date()}")
        
        years = sorted(orders['date'].dt.year.unique())
        print(f"📆 Years covered: {years}")
        print(f"⏱️  Time span: {len(years)} years")
        
        # Check for future data
        if orders['date'].max().year > 2025:
            print(f"⚠️  WARNING: Data contains future dates")
            score -= 20
            issues.append("Data contains unrealistic future dates")
        else:
            print(f"✅ Timeline is realistic")
        
        # Check dataset size
        if len(orders) < 10000:
            print(f"⚠️  WARNING: Dataset size < 10,000 (insufficient for ML)")
            score -= 15
            issues.append(f"Dataset too small: {len(orders)} < 10,000")
        else:
            print(f"✅ Dataset size adequate: {len(orders):,} > 10,000")
        
        # Check dishes
        dishes = orders['dish_name'].nunique()
        print(f"🍽️  Dishes: {dishes}")
    
    # ============================================================
    # 5. MATERIALS COVERAGE
    # ============================================================
    print_section("5. MATERIALS COVERAGE")
    
    if 'recipes' in data and 'inventory' in data:
        recipes = data['recipes']
        inventory = data['inventory']
        
        recipe_materials = set(recipes['material_name'].unique())
        inventory_materials = set(inventory['material_name'].unique())
        
        matching = recipe_materials & inventory_materials
        missing = recipe_materials - inventory_materials
        
        coverage = len(matching) / len(recipe_materials) * 100 if len(recipe_materials) > 0 else 0
        
        print(f"📦 Recipe materials needed: {len(recipe_materials)}")
        print(f"📦 Inventory materials available: {len(inventory_materials)}")
        print(f"✅ Matching materials: {len(matching)}")
        print(f"📊 Coverage: {coverage:.1f}%")
        
        if coverage < 100:
            print(f"❌ Missing {len(missing)} materials: {list(missing)[:5]}")
            score -= 20
            issues.append(f"Missing {len(missing)} materials ({100-coverage:.1f}% gap)")
        else:
            print(f"✅ PERFECT COVERAGE - All materials available!")
    
    # ============================================================
    # 6. FILE STRUCTURE
    # ============================================================
    print_section("6. FILE STRUCTURE")
    
    def count_files(path, ext=''):
        if not os.path.exists(path):
            return 0
        count = 0
        for root, dirs, files in os.walk(path):
            count += len([f for f in files if f.endswith(ext)])
        return count
    
    print(f"📚 Documentation (MD): {count_files('docs', '.md')} files")
    print(f"🎮 Demo scripts: {count_files('scripts/demo', '.py')} files")
    print(f"🛠️  Utility scripts: {count_files('scripts/utils', '.py')} files")
    print(f"🔧 Source modules: {count_files('src', '.py')} files")
    print(f"🧪 Test files: {count_files('tests', '.py')} files")
    
    # Check essential files
    essential_files = [
        'README.md',
        'requirements.txt',
        'app.py',
        'main.py'
    ]
    
    for file in essential_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
            score -= 5
            issues.append(f"Missing essential file: {file}")
    
    # ============================================================
    # 7. FUNCTIONALITY TESTS
    # ============================================================
    print_section("7. FUNCTIONALITY TESTS")
    
    try:
        from cost_analyzer import CostAnalyzer
        analyzer = CostAnalyzer()
        analyzer.load_data(
            'data/csv/recipes_comprehensive.csv',
            'data/csv/inventory_comprehensive.csv',
            'data/csv/orders_real.csv'
        )
        
        # Test cost calculation (correct method is calculate_cogs)
        cost_biryani = analyzer.calculate_cogs('Biryani_Indian')
        cost_pizza = analyzer.calculate_cogs('Pizza_Continental')
        
        print(f"✅ Cost Analyzer working")
        print(f"   • Biryani COGS: ${cost_biryani.get('total_cost', 0):.2f}")
        print(f"   • Pizza COGS: ${cost_pizza.get('total_cost', 0):.2f}")
    except Exception as e:
        print(f"❌ Cost Analyzer failed: {str(e)[:60]}")
        score -= 15
        issues.append(f"Cost Analyzer test failed")
    
    try:
        from inventory_optimizer import InventoryOptimizer
        # Correct: only 2 parameters (use_ml, ml_algorithm)
        optimizer = InventoryOptimizer(use_ml=False)
        optimizer.load_data(
            recipes_file='data/csv/recipes_comprehensive.csv',
            inventory_file='data/csv/inventory_comprehensive.csv',
            orders_file='data/csv/orders_real.csv'
        )
        
        # First generate forecast, then calculate materials
        forecast = optimizer.forecast_demand(days_ahead=7)
        material_req = optimizer.calculate_material_requirements(forecast)
        needs = optimizer.calculate_restocking_needs(material_req)
        
        print(f"✅ Inventory Optimizer working")
        print(f"   • Forecast generated: {len(forecast)} days")
        print(f"   • Materials needing restock: {len(needs)}")
    except Exception as e:
        print(f"❌ Inventory Optimizer failed: {str(e)[:60]}")
        score -= 15
        issues.append(f"Inventory Optimizer test failed")
    
    # ============================================================
    # FINAL REPORT
    # ============================================================
    print_section("📊 FINAL REPORT")
    
    print(f"\n{'─'*60}")
    print(f"  SYSTEM HEALTH SCORE: {score}/100")
    print(f"{'─'*60}\n")
    
    if score >= 95:
        status = "🎯 EXCELLENT - Production Ready++"
        emoji = "🚀"
    elif score >= 85:
        status = "✅ GOOD - Production Ready"
        emoji = "✅"
    elif score >= 70:
        status = "⚠️  WARNING - Needs Attention"
        emoji = "⚠️"
    else:
        status = "❌ CRITICAL - Requires Fixes"
        emoji = "❌"
    
    print(f"{emoji} Status: {status}\n")
    
    if issues:
        print("⚠️  Issues Found:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print()
    else:
        print("✅ No issues found - System is healthy!\n")
    
    # Summary
    print("📋 Summary:")
    print(f"   • Core Modules: {sum(1 for v in modules_status.values() if '✅' in v)}/{len(modules)}")
    print(f"   • Datasets: {len(data)}/3 loaded")
    print(f"   • Materials Coverage: {coverage:.0f}%")
    print(f"   • Data Size: {len(orders):,} orders")
    print(f"   • Timeline: {years[0]}-{years[-1]} ({len(years)} years)")
    print()
    
    # Recommendations
    if score < 100:
        print("💡 Recommendations:")
        if score < 95:
            print("   1. Fix issues listed above")
        if coverage < 100:
            print("   2. Add missing materials to inventory")
        if len(orders) < 10000:
            print("   3. Expand dataset to >10,000 orders")
        print()
    
    print(f"{'='*60}")
    print(f"  Check complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    return score

if __name__ == "__main__":
    score = main()
    sys.exit(0 if score >= 80 else 1)
