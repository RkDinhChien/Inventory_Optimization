# 📊 DATASET GUIDE - ARCHIVE-2

## 🎯 **Overview**

The `archive-2` dataset contains **real food delivery data** with:
- **456,548 records** (119M+ orders)
- **2.8 years** of historical data (145 weeks)
- **51 unique dishes** across 14 categories and 4 cuisines
- **Rich features**: prices, promotions, fulfillment centers

---

## 📁 **Files**

### **1. train.csv** (456,548 records)
Main transaction data:
```
Columns:
- id: Order ID
- week: Week number (1-145)
- center_id: Fulfillment center ID (77 centers)
- meal_id: Meal/dish ID (51 unique)
- checkout_price: Final price paid
- base_price: Original price
- emailer_for_promotion: Email promotion sent (0/1)
- homepage_featured: Featured on homepage (0/1)
- num_orders: Number of orders (TARGET for forecasting)
```

### **2. meal_info.csv** (51 meals)
Meal metadata:
```
Columns:
- meal_id: Unique meal identifier
- category: Beverages, Biryani, Pizza, Pasta, Soup, etc.
- cuisine: Thai, Indian, Italian, Continental
```

### **3. fulfilment_center_info.csv** (77 centers)
Fulfillment center details:
```
Columns:
- center_id: Center identifier
- city_code, region_code: Location info
- center_type: TYPE_A, TYPE_B, TYPE_C
- op_area: Operational area size
```

---

## 🔄 **Conversion Required**

The Inventory Optimization system expects:
```
Required format:
- date: Date (datetime)
- dish_name: Dish name (string)
- quantity_sold: Quantity sold (integer)
```

Archive-2 has:
```
Current format:
- week: Week number (1-145)
- meal_id: Meal ID (integer)
- num_orders: Orders count
```

**Transformation needed:**
1. `week` → `date` (week 1 = 2022-01-03)
2. `meal_id` + `meal_info` → `dish_name` (e.g., "Pizza_Italian")
3. `num_orders` → `quantity_sold`
4. Aggregate by (date, dish) across all centers

---

## 🚀 **Quick Start**

### **Step 1: Inspect Dataset (no dependencies)**
```bash
python3 data/csv/inspect_dataset.py
```

### **Step 2: Install Dependencies**
```bash
pip3 install pandas numpy
```

### **Step 3: Convert Dataset**
```bash
python3 data/csv/convert_archive2_advanced.py
```

This will:
- ✅ Merge train.csv with meal_info.csv
- ✅ Convert week numbers to dates
- ✅ Create dish names (category + cuisine)
- ✅ Aggregate by (date, dish)
- ✅ Generate statistics report
- ✅ Output: `data/csv/orders_real.csv` (~7,395 records)

### **Step 4: Use with System**
```bash
# Test with quick demo
python3 demo_quick.py

# Test with ML
python3 demo_ml.py
```

Or in code:
```python
from src.inventory_optimizer import InventoryOptimizer

optimizer = InventoryOptimizer(use_ml=True, ml_algorithm='xgboost')
optimizer.load_data(orders_file='data/csv/orders_real.csv')

# Forecast next 7 days
forecast = optimizer.forecast_demand(days_ahead=7)
```

---

## 📊 **Dataset Statistics**

### **Size:**
- Original: 456,548 records (~50 MB)
- After aggregation: ~7,395 records (~1 MB)

### **Dishes Breakdown:**
```
Categories (14):
- Beverages: 12 meals
- Pizza, Pasta, Soup: 3 meals each
- Biryani, Desert, Salad, etc.: 3 meals each

Cuisines (4):
- Thai: 15 meals (29%)
- Italian: 12 meals (24%)
- Indian: 12 meals (24%)
- Continental: 12 meals (24%)
```

### **Orders Statistics:**
```
- Total orders: 119,557,485
- Average per record: 261.9 orders
- Max in single record: 24,299 orders
- Average per day: ~15,000 orders
```

### **Time Period:**
```
- Week 1 → 2022-01-03 (Monday)
- Week 145 → 2024-10-14 (Monday)
- Total: 2.8 years of data
```

### **Promotions:**
```
- Email promotions: ~30% of records
- Homepage featured: ~15% of records
- Average discount: 10-15%
```

---

## 🎯 **Use Cases**

### **1. Time Series Forecasting**
- 145 weeks of historical data
- Clear weekly patterns
- Seasonal variations
- Suitable for SARIMA, Prophet

### **2. Multi-location Analysis**
- 77 fulfillment centers
- Regional variations
- Center type comparison

### **3. Promotion Impact**
- Email campaign effectiveness
- Homepage featuring impact
- Price sensitivity analysis

### **4. Dish Performance**
- Category comparison
- Cuisine preferences
- Revenue optimization

---

## ⚠️ **Important Notes**

### **Data Quality:**
- ✅ No missing values in key columns
- ✅ Consistent week numbering
- ✅ All meal_ids have info in meal_info.csv

### **Assumptions:**
- Week 1 = 2022-01-03 (Monday)
- Each week = 7 days
- Aggregation: SUM orders across centers

### **Limitations:**
- No actual material/ingredient data
- Need to create recipes.csv manually
- No inventory/expiry data included

---

## 📝 **Next Steps After Conversion**

1. **Create recipes.csv** (dish → materials mapping)
   ```csv
   dish_name,material_name,quantity_needed
   Pizza_Italian,Flour,0.3
   Pizza_Italian,Cheese,0.2
   ...
   ```

2. **Create inventory.csv** (current stock levels)
   ```csv
   material_name,current_stock,expiry_date,cost_per_unit
   Flour,100,2024-12-31,2.5
   Cheese,50,2024-12-15,5.0
   ...
   ```

3. **Run full system**
   ```bash
   python3 main.py
   ```

---

## 🔗 **Related Files**

- `inspect_dataset.py`: Quick inspection (no dependencies)
- `convert_archive2_advanced.py`: Full conversion with stats
- `convert_archive2.py`: Simple conversion (original)

---

## 📚 **References**

Dataset characteristics:
- Source: Food delivery service (anonymized)
- Period: 2022-2024 (2.8 years)
- Scale: 119M+ orders, 51 dishes, 77 centers
- Format: CSV, UTF-8 encoding

---

**Last Updated**: December 10, 2025  
**Version**: 1.0
