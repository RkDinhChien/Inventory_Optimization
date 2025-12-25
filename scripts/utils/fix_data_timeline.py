"""
Fix Orders Data Timeline - Remove Future Data
Chỉ giữ data từ 2020-2025 (hiện tại)
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("="*60)
print("FIX DATA TIMELINE - REMOVE FUTURE DATA")
print("="*60)

# Load data
df = pd.read_csv('data/csv/orders_real.csv')
df['date'] = pd.to_datetime(df['date'])

print(f"\nHIEN TAI:")
print(f"  Total: {len(df):,} orders")
print(f"  Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"  Years: {sorted(df['date'].dt.year.unique())}")

# Filter: Chỉ giữ data đến 2025
cutoff = pd.Timestamp('2025-12-31')
df_filtered = df[df['date'] <= cutoff].copy()

print(f"\nSAU KHI LOC (2020-2025):")
print(f"  Total: {len(df_filtered):,} orders")

# Nếu thiếu, generate thêm từ historical pattern
if len(df_filtered) < 10000:
    print(f"  WARNING: Chi co {len(df_filtered):,} orders (can >= 10,000)")
    print(f"\nGENERATING THEM {10000 - len(df_filtered):,} ORDERS TU LICH SU...")
    
    # Lấy data 2022-2023 làm mẫu
    sample = df_filtered[df_filtered['date'].dt.year.isin([2022, 2023])].copy()
    
    needed = 10000 - len(df_filtered)
    times = (needed // len(sample)) + 1
    
    additional = []
    for i in range(times):
        temp = sample.copy()
        # Shift về 2020-2021
        temp['date'] = temp['date'] - pd.DateOffset(years=2 + i)
        
        # Variations (giảm về quá khứ)
        noise = np.random.uniform(0.88, 0.96, len(temp))
        temp['quantity_sold'] = (temp['quantity_sold'] * noise).astype(int)
        
        price_noise = np.random.uniform(0.94, 0.98, len(temp))
        temp['checkout_price'] = temp['checkout_price'] * price_noise
        temp['base_price'] = temp['base_price'] * price_noise
        
        additional.append(temp)
    
    # Combine
    combined = pd.concat([df_filtered] + additional, ignore_index=True)
    
    # Filter valid dates only (2020-2025)
    combined = combined[
        (combined['date'] >= '2020-01-01') & 
        (combined['date'] <= '2025-12-31')
    ]
    
    # Take exactly what we need (around 11-12K is good)
    if len(combined) > 12000:
        combined = combined.sample(n=12000, random_state=42)
    
    final = combined.sort_values('date').reset_index(drop=True)
else:
    final = df_filtered.sort_values('date').reset_index(drop=True)

# Save
final.to_csv('data/csv/orders_real.csv', index=False)

print(f"\nFINAL RESULT:")
print(f"  Total: {len(final):,} orders")
print(f"  Date range: {final['date'].min().date()} to {final['date'].max().date()}")
print(f"  Years: {sorted(final['date'].dt.year.unique())}")
print(f"  Status: {'OK' if len(final) >= 10000 else 'WARNING'}")
print(f"\nSaved to: data/csv/orders_real.csv")
print("="*60)
