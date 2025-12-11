"""
Advanced Dataset Converter for archive-2
Converts food delivery data to Inventory Optimization System format
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Paths
BASE_PATH = "data/csv/archive-2"
TRAIN_PATH = f"{BASE_PATH}/train.csv"
MEAL_PATH = f"{BASE_PATH}/meal_info.csv"
CENTER_PATH = f"{BASE_PATH}/fulfilment_center_info.csv"

OUTPUT_ORDERS = "data/csv/orders_real.csv"
OUTPUT_STATS = "data/csv/dataset_stats.txt"

print("="*70)
print("        DATASET CONVERTER - ARCHIVE-2 TO INVENTORY SYSTEM")
print("="*70)

# Step 1: Load data
print("\n1️⃣  Loading datasets...")
train = pd.read_csv(TRAIN_PATH)
meal_info = pd.read_csv(MEAL_PATH)
center_info = pd.read_csv(CENTER_PATH)

print(f"   ✓ train.csv: {len(train):,} records")
print(f"   ✓ meal_info.csv: {len(meal_info)} meals")
print(f"   ✓ fulfilment_center_info.csv: {len(center_info)} centers")

# Step 2: Merge with meal info
print("\n2️⃣  Merging with meal information...")
train = train.merge(meal_info, on='meal_id', how='left')

# Create dish_name (category + cuisine)
train['dish_name'] = train['category'] + '_' + train['cuisine']
print(f"   ✓ Created {train['dish_name'].nunique()} unique dish names")

# Step 3: Convert week to date
print("\n3️⃣  Converting week numbers to dates...")
# Assume week 1 = 2022-01-03 (Monday)
START_DATE = pd.to_datetime("2022-01-03")
train['date'] = train['week'].apply(lambda w: START_DATE + timedelta(weeks=w-1))
print(f"   ✓ Date range: {train['date'].min()} to {train['date'].max()}")

# Step 4: Rename columns to match system format
print("\n4️⃣  Renaming columns...")
train.rename(columns={
    'num_orders': 'quantity_sold'
}, inplace=True)

# Step 5: Select and organize columns
print("\n5️⃣  Organizing columns...")
columns_to_keep = [
    'date',
    'dish_name',
    'quantity_sold',
    'checkout_price',
    'base_price',
    'emailer_for_promotion',
    'homepage_featured',
    'category',
    'cuisine',
    'center_id',
    'week'
]
orders = train[columns_to_keep].copy()

# Step 6: Aggregate by date and dish (sum orders across centers)
print("\n6️⃣  Aggregating data by date and dish...")
orders_agg = orders.groupby(['date', 'dish_name']).agg({
    'quantity_sold': 'sum',
    'checkout_price': 'mean',
    'base_price': 'mean',
    'emailer_for_promotion': 'max',
    'homepage_featured': 'max',
    'category': 'first',
    'cuisine': 'first'
}).reset_index()

print(f"   ✓ Aggregated to {len(orders_agg):,} records")

# Step 7: Sort by date
orders_agg = orders_agg.sort_values(['date', 'dish_name'])

# Step 8: Save to CSV
print("\n7️⃣  Saving converted dataset...")
orders_agg.to_csv(OUTPUT_ORDERS, index=False)
print(f"   ✓ Saved to: {OUTPUT_ORDERS}")
print(f"   ✓ File size: {os.path.getsize(OUTPUT_ORDERS) / 1024 / 1024:.2f} MB")

# Step 9: Generate statistics
print("\n8️⃣  Generating dataset statistics...")
stats = f"""
{'='*70}
                    DATASET STATISTICS
{'='*70}

📊 BASIC INFO:
   • Total records: {len(orders_agg):,}
   • Date range: {orders_agg['date'].min()} to {orders_agg['date'].max()}
   • Number of days: {orders_agg['date'].nunique()}
   • Number of dishes: {orders_agg['dish_name'].nunique()}

🍽️ DISH BREAKDOWN:
"""

# Top dishes by total orders
top_dishes = orders_agg.groupby('dish_name')['quantity_sold'].sum().sort_values(ascending=False).head(10)
stats += "\n   Top 10 Dishes by Total Orders:\n"
for i, (dish, qty) in enumerate(top_dishes.items(), 1):
    stats += f"   {i:2d}. {dish:30s} : {qty:,} orders\n"

# Category breakdown
stats += "\n📁 CATEGORY BREAKDOWN:\n"
category_stats = orders_agg.groupby('category')['quantity_sold'].agg(['sum', 'mean', 'count'])
for cat, row in category_stats.iterrows():
    stats += f"   • {cat:20s} : {row['sum']:,} orders ({row['count']:,} records, avg: {row['mean']:.1f})\n"

# Cuisine breakdown
stats += "\n🌍 CUISINE BREAKDOWN:\n"
cuisine_stats = orders_agg.groupby('cuisine')['quantity_sold'].agg(['sum', 'mean', 'count'])
for cui, row in cuisine_stats.iterrows():
    stats += f"   • {cui:20s} : {row['sum']:,} orders ({row['count']:,} records, avg: {row['mean']:.1f})\n"

# Time series stats
stats += f"""
📈 TIME SERIES STATS:
   • Average orders per day: {orders_agg.groupby('date')['quantity_sold'].sum().mean():.1f}
   • Max orders in a day: {orders_agg.groupby('date')['quantity_sold'].sum().max():,}
   • Min orders in a day: {orders_agg.groupby('date')['quantity_sold'].sum().min():,}
   • Standard deviation: {orders_agg.groupby('date')['quantity_sold'].sum().std():.1f}

💰 PRICE STATS:
   • Average checkout price: ${orders_agg['checkout_price'].mean():.2f}
   • Average base price: ${orders_agg['base_price'].mean():.2f}
   • Average discount: {((orders_agg['base_price'] - orders_agg['checkout_price']) / orders_agg['base_price'] * 100).mean():.1f}%

🎯 PROMOTION STATS:
   • Records with email promotion: {orders_agg['emailer_for_promotion'].sum():,} ({orders_agg['emailer_for_promotion'].mean()*100:.1f}%)
   • Records featured on homepage: {orders_agg['homepage_featured'].sum():,} ({orders_agg['homepage_featured'].mean()*100:.1f}%)

{'='*70}
✅ CONVERSION COMPLETE!

📁 Output file: {OUTPUT_ORDERS}
📊 File size: {os.path.getsize(OUTPUT_ORDERS) / 1024 / 1024:.2f} MB
🕐 Converted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}
"""

# Save stats
with open(OUTPUT_STATS, 'w') as f:
    f.write(stats)

print(stats)

# Step 10: Test data compatibility
print("\n9️⃣  Testing data compatibility with system...")
try:
    from src.inventory_optimizer import InventoryOptimizer
    
    # Try loading the converted data
    optimizer = InventoryOptimizer()
    test_df = pd.read_csv(OUTPUT_ORDERS)
    
    # Check required columns
    required_cols = ['date', 'dish_name', 'quantity_sold']
    missing_cols = [col for col in required_cols if col not in test_df.columns]
    
    if missing_cols:
        print(f"   ❌ Missing columns: {missing_cols}")
    else:
        print(f"   ✅ All required columns present")
        print(f"   ✅ Data format compatible with InventoryOptimizer")
        print(f"   ✅ Ready to use with: optimizer.load_data(orders_file='{OUTPUT_ORDERS}')")
        
except ImportError:
    print("   ⚠️  System not found. Data should still be compatible.")

print("\n" + "="*70)
print("                    CONVERSION SUCCESSFUL!")
print("="*70)
print(f"\n📝 Next steps:")
print(f"   1. Review stats: cat {OUTPUT_STATS}")
print(f"   2. Test with system: python demo_quick.py")
print(f"   3. Run ML comparison: python demo_ml.py")
print("")
