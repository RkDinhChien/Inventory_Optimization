"""
DEMO: EXPIRY MATERIAL RATIO LOGIC
Kiểm tra xem hệ thống có đề xuất món hợp lý dựa trên tỷ lệ nguyên liệu sắp hết hạn
"""

import sys
import pandas as pd
from datetime import datetime, timedelta
from src.inventory_optimizer import InventoryOptimizer

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║         DEMO: EXPIRY MATERIAL RATIO - LOGIC KIỂM TRA HỆ SỐ NVL            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

print("""
📌 VẤN ĐỀ CẦN GIẢI QUYẾT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Không nên đề xuất món ăn chỉ để "tận dụng" một ít nguyên liệu sắp hết hạn,
trong khi phải mua thêm 90% nguyên liệu khác.

VÍ DỤ TỒI:
  Món A cần:
    - Thịt bò sắp hết hạn: 0.2 kg (10% giá trị)
    - Phải mua thêm 5 loại NVL khác: 1.8 kg (90% giá trị)
  → ❌ KHÔNG NÊN đề xuất vì tỷ lệ NVL sắp hết hạn quá thấp (10%)

VÍ DỤ TỐT:
  Món B cần:
    - Bánh mì sắp hết hạn: 1 chiếc (60% giá trị)
    - Thịt sắp hết hạn: 0.1 kg (20% giá trị)
    - Chỉ cần mua rau: 0.05 kg (20% giá trị)
  → ✅ NÊN đề xuất vì tỷ lệ NVL sắp hết hạn cao (80%)

LOGIC MỚI:
  • Tính toán tỷ lệ chi phí NVL sắp hết hạn / Tổng chi phí NVL
  • Chỉ đề xuất mạnh mẽ khi tỷ lệ >= 30%
  • Giảm độ ưu tiên khi tỷ lệ < 30%
""")

# Initialize optimizer
optimizer = InventoryOptimizer()
optimizer.load_data(
    orders_file='data/csv/orders_real.csv',
    inventory_file='data/csv/current_inventory.csv',
    recipes_file='data/csv/recipes.csv'
)

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 PHÂN TÍCH CHI TIẾT TỪNG MÓN ĂN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# Get near expiry materials
near_expiry = optimizer.find_near_expiry_materials(5)
print(f"\n📦 NGUYÊN LIỆU SẮP HẾT HẠN (trong 5 ngày):")
print("─" * 80)
if not near_expiry.empty:
    for _, row in near_expiry.iterrows():
        print(f"  • {row['material_name']:20s} - Còn {row['days_until_expiry']} ngày "
              f"({row['current_stock']:.2f} {row['unit']}) - Giá: ${row['cost_per_unit']:.2f}/{row['unit']}")
else:
    print("  (Không có nguyên liệu sắp hết hạn)")

# Get recommendations
print(f"\n\n🎯 ĐỀ XUẤT MÓN ĂN (có tính toán tỷ lệ NVL sắp hết hạn):")
print("=" * 80)

recommendations = optimizer.recommend_dishes(max_recommendations=10)

if not recommendations.empty:
    for idx, rec in recommendations.iterrows():
        print(f"\n{'─' * 80}")
        print(f"#{idx + 1}. {rec['dish_name']}")
        print(f"{'─' * 80}")
        
        # Get recipe details
        dish_recipes = optimizer.recipes_data[
            optimizer.recipes_data['dish_name'] == rec['dish_name']
        ]
        
        print(f"\n📋 CÔNG THỨC & PHÂN TÍCH:")
        total_cost = 0
        expiry_cost = 0
        
        for _, recipe_row in dish_recipes.iterrows():
            material_name = recipe_row['material_name']
            qty_needed = recipe_row['quantity_needed']
            
            # Get material info
            material_info = optimizer.inventory_data[
                optimizer.inventory_data['material_name'] == material_name
            ].iloc[0]
            
            cost_per_unit = material_info['cost_per_unit']
            material_cost = qty_needed * cost_per_unit
            total_cost += material_cost
            
            # Check if expiring
            is_expiring = material_name in rec['expiring_materials_used']
            if is_expiring:
                expiry_cost += material_cost
                expiry_marker = " ⚠️  SẮP HẾT HẠN"
            else:
                expiry_marker = ""
            
            material_ratio = (material_cost / total_cost * 100) if total_cost > 0 else 0
            
            print(f"  • {material_name:20s}: {qty_needed:.2f} → "
                  f"${material_cost:.2f} ({material_ratio:.1f}% giá trị){expiry_marker}")
        
        # Summary
        expiry_ratio = (expiry_cost / total_cost * 100) if total_cost > 0 else 0
        non_expiry_ratio = 100 - expiry_ratio
        
        print(f"\n💰 CHI PHÍ PHÂN TÍCH:")
        print(f"  • Tổng chi phí món:           ${total_cost:.2f}")
        print(f"  • Chi phí NVL sắp hết hạn:    ${expiry_cost:.2f} ({expiry_ratio:.1f}%)")
        print(f"  • Chi phí NVL khác/phải mua:  ${total_cost - expiry_cost:.2f} ({non_expiry_ratio:.1f}%)")
        
        print(f"\n📊 ĐÁNH GIÁ:")
        print(f"  • Tỷ lệ NVL sắp hết hạn:      {rec['expiry_material_ratio']:.1f}%")
        print(f"  • Điểm đề xuất:               {rec['recommendation_score']:.2f}")
        print(f"  • Điểm khẩn cấp (expiry):     {rec['expiry_urgency_score']:.2f}")
        print(f"  • Có thể làm tối đa:          {rec['max_servings_possible']} phần")
        
        # Verdict
        print(f"\n✅ KẾT LUẬN:")
        if rec['expiry_material_ratio'] >= 50:
            print(f"  🌟 ĐÁNH GIÁ: XUẤT SẮC! Tỷ lệ NVL sắp hết hạn rất cao ({rec['expiry_material_ratio']:.1f}%)")
            print(f"     → Nên ưu tiên làm món này để tận dụng tối đa NVL sắp hết hạn")
        elif rec['expiry_material_ratio'] >= 30:
            print(f"  👍 ĐÁNH GIÁ: TỐT! Tỷ lệ NVL sắp hết hạn hợp lý ({rec['expiry_material_ratio']:.1f}%)")
            print(f"     → Có thể làm món này để giảm lãng phí")
        elif rec['expiry_material_ratio'] > 0:
            print(f"  ⚠️  ĐÁNH GIÁ: THẤP! Tỷ lệ NVL sắp hết hạn chỉ {rec['expiry_material_ratio']:.1f}%")
            print(f"     → Không nên ưu tiên vì phải mua thêm {non_expiry_ratio:.1f}% NVL khác")
        else:
            print(f"  ℹ️  ĐÁNH GIÁ: Món này không sử dụng NVL sắp hết hạn")
            print(f"     → Đề xuất dựa trên sẵn có và mùa vụ")

print(f"\n\n{'=' * 80}")
print(f"📊 BẢNG TỔNG HỢP:")
print(f"{'=' * 80}")
print(f"\n{recommendations[['dish_name', 'expiry_material_ratio', 'recommendation_score', 'expiry_urgency_score', 'max_servings_possible']].to_string(index=False)}")

print(f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 KẾT LUẬN VÀ KHUYẾN NGHỊ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. LOGIC MỚI ĐÃ ĐƯỢC THÊM VÀO:
   ✅ Tính toán tỷ lệ chi phí NVL sắp hết hạn / Tổng chi phí
   ✅ Hiển thị rõ ràng tỷ lệ % trong kết quả
   ✅ Giảm điểm ưu tiên nếu tỷ lệ < 30%
   ✅ Chỉ đề xuất mạnh khi tỷ lệ >= 30%

2. CÁCH ĐÁNH GIÁ:
   • >= 50%: XUẤT SẮC - Ưu tiên cao
   • >= 30%: TỐT - Có thể làm
   • < 30%:  THẤP - Không ưu tiên (vì phải mua quá nhiều NVL khác)

3. LỢI ÍCH:
   ✅ Tránh lãng phí chi phí mua NVL mới
   ✅ Tối ưu hóa việc tận dụng NVL sắp hết hạn
   ✅ Quyết định kinh doanh thông minh hơn

4. ÁP DỤNG:
   • Hệ thống tự động tính toán tỷ lệ này
   • Điểm "expiry_urgency_score" sẽ giảm 80% nếu tỷ lệ < 30%
   • Kết quả: Món có tỷ lệ thấp sẽ không xuất hiện ở top recommendations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ DEMO HOÀN THÀNH - LOGIC ĐÃ ĐƯỢC CẢI TIẾN!
""")
