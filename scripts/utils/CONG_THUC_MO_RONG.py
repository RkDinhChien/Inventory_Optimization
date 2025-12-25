"""
CÔNG THỨC DỰ ĐOÁN MỞ RỘNG
Tích hợp thêm các yếu tố thị trường, kinh tế, xã hội
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║           CÔNG THỨC DỰ ĐOÁN MỞ RỘNG - YẾU TỐ THỊ TRƯỜNG                  ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

print("""
📊 HIỆN TẠI: Chỉ dùng LỊCH SỬ ĐẶT MÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Statistical Method:
   y = μ × s × w
   
   • μ = Trung bình lịch sử
   • s = Hệ số mùa vụ (weekday pattern)
   • w = Hệ số cuối tuần

XGBoost Method:
   ŷ = Σ f_k(X) với 17 features
   
   • 17 features CHỈ về TIME (thời gian):
     - day_of_week, day_of_month, month, quarter
     - day_sin, day_cos, month_sin, month_cos
     - is_weekend, is_month_start, is_month_end...

⚠️ VẤN ĐỀ:
   • Không tính yếu tố THỜI TIẾT
   • Không tính yếu tố KINH TẾ (giá cả, lương)
   • Không tính yếu tố XÃ HỘI (events, lễ hội)
   • Không tính yếu tố ĐỐI THỦ (competitor actions)
   • Không tính yếu tố MARKETING (promotions, ads)
""")

print("""
🌍 MỞ RỘNG: TÍCH HỢP YẾU TỐ THỊ TRƯỜNG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CÔNG THỨC TỔNG QUÁT MỞ RỘNG:
────────────────────────────

    ŷ = f(Time, Weather, Economy, Social, Competition, Marketing, Internal)

Chi tiết từng nhóm yếu tố:
─────────────────────────
""")

print("""
1️⃣  YẾU TỐ THỜI GIAN (Time Factors) - ĐÃ CÓ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Features hiện tại (17 features):
────────────────────────────────

• day_of_week (0-6): Thứ 2-CN
• day_of_month (1-31): Ngày trong tháng
• month (1-12): Tháng trong năm
• quarter (1-4): Quý
• week_of_year (1-52): Tuần trong năm
• day_of_year (1-365): Ngày trong năm
• is_weekend (0/1): Cuối tuần
• day_sin, day_cos: Cyclical encoding ngày
• month_sin, month_cos: Cyclical encoding tháng
• is_month_start, is_month_end: Đầu/cuối tháng
• is_quarter_start, is_quarter_end: Đầu/cuối quý
• is_year_start, is_year_end: Đầu/cuối năm

✅ Đã implement
""")

print("""
2️⃣  YẾU TỐ THỜI TIẾT (Weather Factors) - MỚI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lý do quan trọng:
────────────────

• Mưa → Khách gọi delivery nhiều hơn
• Nóng → Ưa thích đồ mát (salad, soup lạnh)
• Lạnh → Ưa thích đồ nóng (phở, soup nóng)
• Bão/Lũ → Giảm đơn hàng drastically

Data cần thu thập:
──────────────────

┌────────────────────────┬──────────────┬─────────────────┐
│ Feature                │ Range        │ Data Source     │
├────────────────────────┼──────────────┼─────────────────┤
│ temperature            │ -10 to 45°C  │ Weather API     │
│ humidity               │ 0-100%       │ Weather API     │
│ precipitation          │ 0-100mm      │ Weather API     │
│ wind_speed             │ 0-50 km/h    │ Weather API     │
│ weather_condition      │ 0-10         │ Weather API     │
│  (0=sunny, 5=rainy,    │              │                 │
│   8=storm, 10=typhoon) │              │                 │
│ air_quality_index (AQI)│ 0-500        │ AQI API         │
│ feels_like_temp        │ -15 to 50°C  │ Weather API     │
└────────────────────────┴──────────────┴─────────────────┘

Công thức mở rộng:
─────────────────

Statistical Enhancement:
   y = μ × s × w × weather_factor
   
   weather_factor = {
       sunny: 1.0
       cloudy: 0.95
       light_rain: 1.1  (delivery tăng)
       heavy_rain: 0.7  (giảm mạnh)
       storm: 0.3       (giảm rất mạnh)
   }

XGBoost Enhancement:
   Add 8 weather features → Total: 17 + 8 = 25 features
   
   • temperature
   • humidity
   • precipitation
   • wind_speed
   • weather_condition
   • AQI
   • feels_like_temp
   • is_extreme_weather (0/1)

Ví dụ thực tế:
─────────────

Scenario 1: Ngày nắng đẹp
   • temperature = 28°C (perfect)
   • humidity = 60%
   • precipitation = 0mm
   → Base forecast: 50 phần
   → Weather factor: 1.0
   → Final: 50 phần

Scenario 2: Mưa lớn
   • temperature = 24°C
   • precipitation = 30mm (heavy rain)
   • humidity = 95%
   → Base forecast: 50 phần
   → Weather factor: 0.7 (giảm 30%)
   → Final: 35 phần
   
   BUT: Delivery orders tăng!
   → Delivery forecast: +40%
   → Delivery: 70 phần!

Scenario 3: Bão lớn
   • wind_speed = 80 km/h (typhoon)
   • precipitation = 100mm+
   → Weather factor: 0.1 (giảm 90%)
   → Final: 5 phần (chỉ order trước)

API Integration:
───────────────

import requests

def get_weather_features(date, location):
    # OpenWeatherMap API
    api_key = "YOUR_API_KEY"
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": 10.8231,  # Ho Chi Minh City
        "lon": 106.6297,
        "appid": api_key,
        "units": "metric"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "precipitation": data.get("rain", {}).get("3h", 0),
        "wind_speed": data["wind"]["speed"],
        "weather_condition": data["weather"][0]["id"],
        "feels_like": data["main"]["feels_like"]
    }
""")

print("""
3️⃣  YẾU TỐ KINH TẾ (Economic Factors) - MỚI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lý do quan trọng:
────────────────

• Lương về (ngày 1-5) → Tăng chi tiêu
• Cuối tháng (ngày 25-31) → Giảm chi tiêu
• Lạm phát cao → Chuyển sang món rẻ
• Giá nguyên liệu tăng → Phải tăng giá → Giảm đơn
• Khủng hoảng kinh tế → Giảm đơn hàng

Data cần thu thập:
──────────────────

┌──────────────────────────┬──────────────┬─────────────────┐
│ Feature                  │ Range        │ Data Source     │
├──────────────────────────┼──────────────┼─────────────────┤
│ is_payday_week           │ 0/1          │ Calendar        │
│  (tuần lương về)         │              │                 │
│ days_since_payday        │ 0-30         │ Calendar        │
│ inflation_rate           │ 0-20%        │ Central Bank    │
│ consumer_price_index     │ 100-300      │ Government Data │
│ unemployment_rate        │ 0-15%        │ Government Data │
│ average_income_growth    │ -10 to +20%  │ Statistics Dept │
│ fuel_price               │ 15-30k VND/L │ Market Data     │
│ food_price_index         │ 100-200      │ Market Data     │
│ competitor_avg_price     │ 30-100k VND  │ Market Research │
└──────────────────────────┴──────────────┴─────────────────┘

Công thức mở rộng:
─────────────────

Statistical Enhancement:
   y = μ × s × w × weather_factor × economic_factor
   
   economic_factor = {
       payday_week (1-7): 1.3        # Tăng 30%
       mid_month (8-20): 1.0          # Bình thường
       end_month (21-30): 0.8         # Giảm 20%
   }
   
   × price_sensitivity_factor
   
   price_sensitivity = {
       low_inflation (<3%): 1.0
       medium_inflation (3-7%): 0.95
       high_inflation (>7%): 0.85
   }

XGBoost Enhancement:
   Add 9 economic features → Total: 25 + 9 = 34 features

Ví dụ thực tế:
─────────────

Scenario 1: Đầu tháng (lương mới về)
   • is_payday_week = 1
   • days_since_payday = 2
   • inflation_rate = 4% (stable)
   → Base forecast: 50 phần
   → Economic factor: 1.3
   → Final: 65 phần (tăng 30%)

Scenario 2: Cuối tháng (hết tiền)
   • days_since_payday = 28
   • is_payday_week = 0
   → Base forecast: 50 phần
   → Economic factor: 0.8
   → Final: 40 phần (giảm 20%)

Scenario 3: Lạm phát cao
   • inflation_rate = 12%
   • food_price_index = 180 (cao)
   • consumer_price_index = 150
   → Base forecast: 50 phần
   → Price sensitivity: 0.75
   → Final: 37 phần (giảm 25%)
   
   BUT: Món rẻ tăng!
   • Cơm Tấm (rẻ): +20%
   • Phở Bò (đắt): -40%

Integration:
───────────

def get_economic_features(date):
    return {
        "is_payday_week": 1 if date.day <= 7 else 0,
        "days_since_payday": (date.day - 1) % 30,
        "inflation_rate": get_inflation_rate(),  # API
        "consumer_price_index": get_cpi(),        # API
        "fuel_price": get_fuel_price(),           # Web scraping
        "food_price_index": get_food_index()      # API
    }
""")

print("""
4️⃣  YẾU TỐ XÃ HỘI (Social Factors) - MỚI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lý do quan trọng:
────────────────

• Lễ Tết → Tăng đơn hàng x3-5
• World Cup → Tăng đơn món ăn vặt
• Ngày lễ tình nhân → Tăng đơn romantic
• Khai trường → Tăng đơn lunch
• COVID/Dịch bệnh → Giảm đơn drastically

Data cần thu thập:
──────────────────

┌────────────────────────────┬──────────────┬─────────────────┐
│ Feature                    │ Range        │ Data Source     │
├────────────────────────────┼──────────────┼─────────────────┤
│ is_public_holiday          │ 0/1          │ Calendar API    │
│ is_lunar_new_year_week     │ 0/1          │ Lunar Calendar  │
│ is_major_holiday           │ 0/1          │ Calendar        │
│  (30/4, 1/5, 2/9...)       │              │                 │
│ is_school_holiday          │ 0/1          │ School Calendar │
│ is_exam_week               │ 0/1          │ School Calendar │
│ is_sports_event            │ 0/1          │ Sports API      │
│  (World Cup, SEA Games)    │              │                 │
│ is_festival                │ 0/1          │ Events Calendar │
│  (Food festival, concerts) │              │                 │
│ is_religious_day           │ 0/1          │ Religious Cal   │
│  (Rằm, Vu Lan...)          │              │                 │
│ days_to_next_holiday       │ 0-90         │ Calendar        │
│ population_nearby          │ 1k-500k      │ Census Data     │
│ traffic_density            │ 0-100        │ Google Maps API │
│ covid_restriction_level    │ 0-5          │ Government      │
└────────────────────────────┴──────────────┴─────────────────┘

Công thức mở rộng:
─────────────────

Statistical Enhancement:
   y = μ × s × w × weather_factor × economic_factor × social_factor
   
   social_factor = {
       lunar_new_year: 5.0        # Tăng 400%!
       major_holiday: 2.0          # Tăng 100%
       normal_day: 1.0
       exam_week: 0.7              # Giảm 30%
       covid_lockdown: 0.2         # Giảm 80%
   }

XGBoost Enhancement:
   Add 12 social features → Total: 34 + 12 = 46 features

Ví dụ thực tế:
─────────────

Scenario 1: Tết Nguyên Đán
   • is_lunar_new_year_week = 1
   • is_public_holiday = 1
   • days_to_next_holiday = 0
   → Base forecast: 50 phần
   → Social factor: 5.0
   → Final: 250 phần! (tăng 400%)
   
   Breakdown:
   • Gà luộc: +500% (món Tết)
   • Bánh chưng: +1000%
   • Phở: -20% (ít người ăn)

Scenario 2: World Cup Finals
   • is_sports_event = 1
   • is_weekend = 1
   • time = evening
   → Base forecast: 50 phần
   → Social factor: 2.5
   → Final: 125 phần
   
   Breakdown:
   • Bia: +300%
   • Đồ ăn vặt: +250%
   • Món chính: +50%

Scenario 3: COVID Lockdown
   • covid_restriction_level = 5 (strict)
   • is_public_gathering_banned = 1
   → Base forecast: 50 phần
   → Social factor: 0.2
   → Final: 10 phần (giảm 80%)
   
   BUT: Delivery ONLY
   • Delivery: 45 phần (+350%)

Scenario 4: Tuần thi cử
   • is_exam_week = 1
   • is_school_holiday = 0
   → Base forecast: 50 phần (lunch)
   → Social factor: 0.7
   → Final: 35 phần (giảm 30%)

Integration:
───────────

import requests
from datetime import datetime

def get_social_features(date):
    # Check holidays
    is_holiday = check_public_holiday(date)
    is_tet = check_lunar_new_year(date)
    
    # Check events
    sports_events = get_sports_events(date)  # API
    festivals = get_festivals(date)          # Events API
    
    # Check restrictions
    covid_level = get_covid_restriction()    # Gov API
    
    return {
        "is_public_holiday": is_holiday,
        "is_lunar_new_year_week": is_tet,
        "is_sports_event": 1 if sports_events else 0,
        "is_festival": 1 if festivals else 0,
        "covid_restriction_level": covid_level,
        "traffic_density": get_traffic_data(date)  # Google API
    }
""")

print("""
5️⃣  YẾU TỐ ĐỐI THỦ (Competition Factors) - MỚI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lý do quan trọng:
────────────────

• Đối thủ giảm giá → Mất khách
• Đối thủ mở chi nhánh mới → Giảm đơn
• Đối thủ đóng cửa → Tăng đơn
• Đối thủ chạy promotion → Giảm đơn
• Review xấu của đối thủ → Tăng đơn

Data cần thu thập:
──────────────────

┌────────────────────────────┬──────────────┬─────────────────┐
│ Feature                    │ Range        │ Data Source     │
├────────────────────────────┼──────────────┼─────────────────┤
│ num_competitors_nearby     │ 0-50         │ Google Maps     │
│ avg_competitor_rating      │ 1.0-5.0      │ Review Sites    │
│ avg_competitor_price       │ 20-150k VND  │ Menu Analysis   │
│ competitor_promotion_count │ 0-10         │ Social Media    │
│ new_competitor_opened      │ 0/1          │ Business License│
│ competitor_closed          │ 0/1          │ Business Data   │
│ price_difference_ratio     │ -50 to +50%  │ Price Compare   │
│ rating_difference          │ -2.0 to +2.0 │ Review Compare  │
│ competitor_delivery_fee    │ 0-30k VND    │ App Data        │
│ market_share_estimate      │ 0-100%       │ Order Volume    │
└────────────────────────────┴──────────────┴─────────────────┘

Công thức mở rộng:
─────────────────

Statistical Enhancement:
   y = μ × s × w × weather × economic × social × competition_factor
   
   competition_factor = {
       no_competitors: 1.5            # Độc quyền!
       low_competition (1-3): 1.2
       medium_competition (4-7): 1.0
       high_competition (8+): 0.8
       
       competitor_promotion: 0.7      # Giảm 30%
       new_competitor: 0.85           # Giảm 15%
       competitor_closed: 1.2         # Tăng 20%
   }

XGBoost Enhancement:
   Add 10 competition features → Total: 46 + 10 = 56 features

Ví dụ thực tế:
─────────────

Scenario 1: Đối thủ chạy promotion 50%
   • competitor_promotion_count = 3
   • price_difference_ratio = +50% (ta đắt hơn)
   → Base forecast: 50 phần
   → Competition factor: 0.7
   → Final: 35 phần (mất 15 phần cho đối thủ)

Scenario 2: Đối thủ lớn đóng cửa
   • competitor_closed = 1
   • market_share_gain = +15%
   → Base forecast: 50 phần
   → Competition factor: 1.2
   → Final: 60 phần (ăn phần đối thủ)

Scenario 3: Review ta tốt hơn đối thủ
   • rating_difference = +1.2 (ta 4.8, họ 3.6)
   • avg_competitor_rating = 3.6
   → Base forecast: 50 phần
   → Competition factor: 1.15
   → Final: 57 phần

Integration:
───────────

def get_competition_features(location):
    # Scrape Google Maps
    competitors = get_nearby_restaurants(location, radius=1000)
    
    # Analyze prices
    competitor_prices = scrape_competitor_menus()
    
    # Check promotions
    promotions = monitor_competitor_social_media()
    
    return {
        "num_competitors_nearby": len(competitors),
        "avg_competitor_rating": np.mean([c.rating for c in competitors]),
        "avg_competitor_price": np.mean(competitor_prices),
        "competitor_promotion_count": len(promotions),
        "price_difference_ratio": (my_price - avg_price) / avg_price
    }
""")

print("""
6️⃣  YẾU TỐ MARKETING (Marketing Factors) - MỚI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lý do quan trọng:
────────────────

• Chạy ads → Tăng đơn +30-50%
• Promotion/Discount → Tăng đơn +50-100%
• Influencer review → Tăng đơn +200%
• Social media viral → Tăng đơn +500%
• Email campaign → Tăng đơn +15%

Data cần thu thập:
──────────────────

┌────────────────────────────┬──────────────┬─────────────────┐
│ Feature                    │ Range        │ Data Source     │
├────────────────────────────┼──────────────┼─────────────────┤
│ is_promotion_active        │ 0/1          │ Internal DB     │
│ discount_percentage        │ 0-70%        │ Promotion DB    │
│ days_since_last_promotion  │ 0-90         │ Promotion DB    │
│ ad_spend_today             │ 0-10M VND    │ Ads Platform    │
│ ad_impressions             │ 0-1M         │ Facebook/Google │
│ ad_clicks                  │ 0-50k        │ Ads Analytics   │
│ social_media_mentions      │ 0-10k        │ Social Monitor  │
│ influencer_posts           │ 0-20         │ Influencer Track│
│ email_sent_count           │ 0-100k       │ Email Platform  │
│ email_open_rate            │ 0-100%       │ Email Analytics │
│ viral_content_score        │ 0-100        │ Social Analytics│
│ brand_search_volume        │ 0-10k        │ Google Trends   │
│ review_count_this_week     │ 0-500        │ Review Platform │
│ avg_review_rating_this_week│ 1.0-5.0      │ Review Platform │
└────────────────────────────┴──────────────┴─────────────────┘

Công thức mở rộng:
─────────────────

Statistical Enhancement:
   y = μ × s × w × weather × economic × social × 
       competition × marketing_factor
   
   marketing_factor = {
       no_promotion: 1.0
       discount_10_20%: 1.3           # Tăng 30%
       discount_30_50%: 1.8           # Tăng 80%
       discount_50%+: 2.5             # Tăng 150%
       
       influencer_post: 2.0           # Tăng 100%
       viral_content: 5.0             # Tăng 400%!
       
       ad_campaign: 1.2-1.5           # Tùy budget
   }

XGBoost Enhancement:
   Add 14 marketing features → Total: 56 + 14 = 70 features

Ví dụ thực tế:
─────────────

Scenario 1: Flash Sale 50%
   • is_promotion_active = 1
   • discount_percentage = 50%
   • ad_spend_today = 5M VND
   • ad_impressions = 500k
   → Base forecast: 50 phần
   → Marketing factor: 2.5
   → Final: 125 phần (tăng 150%)
   
   Note: Margin giảm 50% nhưng volume x2.5!

Scenario 2: Influencer Review (1M followers)
   • influencer_posts = 1
   • social_media_mentions = 5000
   • viral_content_score = 85
   → Base forecast: 50 phần
   → Marketing factor: 3.0
   → Final: 150 phần (tăng 200%)
   
   Kéo dài 3-7 ngày!

Scenario 3: Email Campaign
   • email_sent_count = 50k
   • email_open_rate = 25%
   • ad_clicks = 2500
   → Base forecast: 50 phần
   → Marketing factor: 1.15
   → Final: 57 phần (tăng 15%)

Scenario 4: Viral TikTok (5M views)
   • viral_content_score = 95
   • social_media_mentions = 50k
   • brand_search_volume = +800%
   → Base forecast: 50 phần
   → Marketing factor: 6.0
   → Final: 300 phần! (tăng 500%)
   
   PROBLEM: Không đủ nguyên liệu!

Integration:
───────────

def get_marketing_features(date):
    # Check promotions
    promotion = get_active_promotions(date)
    
    # Get ads data
    ads_data = get_ads_performance(date)  # FB/Google API
    
    # Social media monitoring
    social_data = monitor_social_media()  # Hootsuite API
    
    # Email campaigns
    email_data = get_email_stats(date)    # Mailchimp API
    
    return {
        "is_promotion_active": 1 if promotion else 0,
        "discount_percentage": promotion.discount if promotion else 0,
        "ad_spend_today": ads_data["spend"],
        "ad_impressions": ads_data["impressions"],
        "social_media_mentions": social_data["mentions"],
        "viral_content_score": calculate_viral_score(social_data)
    }
""")

print("""
7️⃣  YẾU TỐ NỘI BỘ (Internal Factors) - MỚI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Lý do quan trọng:
────────────────

• Thiếu nhân viên → Giảm đơn (slow service)
• Menu mới → Tăng đơn (+15%)
• Đổi đầu bếp → Thay đổi chất lượng
• Máy móc hỏng → Giảm đơn
• Out of stock → Mất đơn

Data cần thu thập:
──────────────────

┌────────────────────────────┬──────────────┬─────────────────┐
│ Feature                    │ Range        │ Data Source     │
├────────────────────────────┼──────────────┼─────────────────┤
│ staff_available            │ 0-50         │ HR System       │
│ staff_experience_avg_years │ 0-20         │ HR System       │
│ is_new_menu_item           │ 0/1          │ Menu DB         │
│ days_since_menu_change     │ 0-180        │ Menu DB         │
│ kitchen_capacity_util      │ 0-100%       │ IoT Sensors     │
│ average_prep_time_mins     │ 5-60         │ Kitchen System  │
│ ingredient_availability    │ 0-100%       │ Inventory System│
│ equipment_status           │ 0-100%       │ Maintenance Log │
│ order_fulfillment_rate     │ 0-100%       │ POS System      │
│ customer_wait_time_avg     │ 0-120 mins   │ POS System      │
│ delivery_time_avg          │ 10-90 mins   │ Delivery System │
│ return_rate                │ 0-20%        │ Customer Service│
│ complaint_count_this_week  │ 0-100        │ Support Tickets │
└────────────────────────────┴──────────────┴─────────────────┘

Công thức mở rộng:
─────────────────

Statistical Enhancement:
   y = μ × s × w × weather × economic × social × 
       competition × marketing × internal_factor
   
   internal_factor = {
       full_staff: 1.0
       understaffed (-30%): 0.8       # Giảm 20%
       overstaffed (+30%): 0.95       # Phí không hiệu quả
       
       new_menu_item: 1.15            # Tăng 15% (curiosity)
       ingredient_shortage: 0.7       # Giảm 30%
       equipment_broken: 0.5          # Giảm 50%
   }

XGBoost Enhancement:
   Add 13 internal features → Total: 70 + 13 = 83 features

Ví dụ thực tế:
─────────────

Scenario 1: Thiếu nhân viên (50%)
   • staff_available = 3 (normal: 6)
   • kitchen_capacity_util = 40%
   • average_prep_time_mins = 45 (normal: 25)
   → Base forecast: 50 phần
   → Internal factor: 0.75
   → Final: 37 phần (không đủ capacity)

Scenario 2: Launch món mới
   • is_new_menu_item = 1
   • days_since_menu_change = 2
   • social_media_mentions = +200%
   → Base forecast: 50 phần
   → Internal factor: 1.15
   → Marketing boost: 1.3
   → Final: 75 phần

Scenario 3: Out of stock beef
   • ingredient_availability = 60% (thiếu beef)
   • order_fulfillment_rate = 70%
   • return_rate = 15%
   → Base forecast: 50 phần Phở Bò
   → Internal factor: 0.6
   → Final: 30 phần (mất 20 phần)
   
   → Need emergency restock!

Integration:
───────────

def get_internal_features():
    # HR data
    staff = get_staff_schedule()
    
    # Kitchen IoT
    kitchen_status = get_kitchen_sensors()
    
    # Inventory
    inventory = get_current_inventory()
    
    # POS data
    pos_metrics = get_pos_metrics()
    
    return {
        "staff_available": len(staff),
        "kitchen_capacity_util": kitchen_status["utilization"],
        "ingredient_availability": calculate_availability(inventory),
        "order_fulfillment_rate": pos_metrics["fulfillment_rate"],
        "average_prep_time_mins": pos_metrics["avg_prep_time"]
    }
""")

print("""
🚀 CÔNG THỨC TỔNG HỢP CUỐI CÙNG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STATISTICAL METHOD (Enhanced):
──────────────────────────────

y = μ × s × w × f_weather × f_economic × f_social × 
    f_competition × f_marketing × f_internal

Trong đó:
• μ = Trung bình lịch sử
• s = Hệ số mùa vụ (seasonal)
• w = Hệ số cuối tuần (weekend)
• f_weather = Weather factor (0.3-1.1)
• f_economic = Economic factor (0.75-1.3)
• f_social = Social factor (0.2-5.0)
• f_competition = Competition factor (0.7-1.5)
• f_marketing = Marketing factor (1.0-6.0)
• f_internal = Internal factor (0.5-1.15)

Ví dụ tính toán:
───────────────

Base: μ = 50 phần/ngày

Scenario: Tết + Promotion + Mưa
• s = 1.0 (Tết không có pattern)
• w = 1.0 (không quan trọng)
• f_weather = 1.1 (mưa → delivery tăng)
• f_economic = 1.3 (lương về)
• f_social = 5.0 (Tết!)
• f_competition = 1.2 (đối thủ đóng cửa)
• f_marketing = 1.5 (chạy ads)
• f_internal = 1.0 (full staff)

y = 50 × 1.0 × 1.0 × 1.1 × 1.3 × 5.0 × 1.2 × 1.5 × 1.0
y = 50 × 12.87
y = 643 phần!

→ Cần chuẩn bị GẤP 13 LẦN bình thường!


XGBOOST METHOD (Enhanced):
───────────────────────────

Total Features: 83 features
├─ Time: 17 features (existing)
├─ Weather: 8 features
├─ Economic: 9 features
├─ Social: 12 features
├─ Competition: 10 features
├─ Marketing: 14 features
└─ Internal: 13 features

Model Architecture:
   ŷ = Σ(k=1 to K) f_k(X₁, X₂, ..., X₈₃)
   
   Với K = 100-1000 decision trees

Feature Importance (Expected):
   1. is_lunar_new_year_week: 18%
   2. discount_percentage: 12%
   3. temperature: 8%
   4. is_payday_week: 7%
   5. day_of_week: 6%
   6. precipitation: 5%
   7. competitor_promotion_count: 4%
   8. staff_available: 4%
   ... (còn 75 features)

Accuracy Expected:
   • Current (17 features): 90-95%
   • Enhanced (83 features): 95-98%
   
   Improvement: +3-5% accuracy!


IMPLEMENTATION ROADMAP:
───────────────────────

Phase 1: Quick Wins (Week 1-2)
   ✓ Add weather data (8 features)
   ✓ Add economic calendar (payday, holidays)
   → Expected: +2% accuracy

Phase 2: External Data (Week 3-4)
   ✓ Integrate social events
   ✓ Monitor competitors
   → Expected: +1.5% accuracy

Phase 3: Marketing Integration (Week 5-6)
   ✓ Connect ads platforms
   ✓ Social media monitoring
   → Expected: +1% accuracy

Phase 4: Internal Systems (Week 7-8)
   ✓ IoT sensors
   ✓ Staff scheduling
   ✓ Real-time inventory
   → Expected: +0.5% accuracy

Total: 90% → 95% accuracy (+5%)
""")

print("""
📊 SO SÁNH: HIỆN TẠI VS MỞ RỘNG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────┬──────────────┬──────────────┬──────────────┐
│ Aspect              │ Current      │ Enhanced     │ Improvement  │
├─────────────────────┼──────────────┼──────────────┼──────────────┤
│ Features            │ 17           │ 83           │ +388%        │
│ Data Sources        │ 1 (orders)   │ 7 sources    │ +600%        │
│ Accuracy            │ 90-95%       │ 95-98%       │ +3-5%        │
│ Prediction Range    │ 1-30 days    │ 1-90 days    │ +200%        │
│ Special Events      │ ❌            │ ✅            │ NEW          │
│ Weather Impact      │ ❌            │ ✅            │ NEW          │
│ Competition         │ ❌            │ ✅            │ NEW          │
│ Marketing ROI       │ ❌            │ ✅            │ NEW          │
│ Real-time Adjust    │ ❌            │ ✅            │ NEW          │
│ Setup Time          │ 1 day        │ 2 months     │ Complex      │
│ Maintenance         │ Low          │ High         │ More work    │
│ Cost                │ $0           │ $500-2k/mo   │ APIs, tools  │
└─────────────────────┴──────────────┴──────────────┴──────────────┘

ROI Analysis:
────────────

Current System:
• Accuracy: 90%
• Waste: 10% = $3,000/month
• Cost: $0

Enhanced System:
• Accuracy: 96%
• Waste: 4% = $1,200/month
• Savings: $1,800/month
• Cost: $1,000/month (APIs + maintenance)
• NET GAIN: $800/month = $9,600/year

ROI: 960% year 1!

Worth it? YES for medium-large restaurants!
""")

print("""
💡 NEXT STEPS - IMPLEMENT NGAY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Weather Integration (EASY - 1 ngày)
───────────────────────────────────────────

import requests

# OpenWeatherMap API (FREE tier: 1000 calls/day)
API_KEY = "your_key_here"

def add_weather_features(df):
    for idx, row in df.iterrows():
        weather = get_weather(row['date'])
        df.loc[idx, 'temperature'] = weather['temp']
        df.loc[idx, 'precipitation'] = weather['rain']
        df.loc[idx, 'humidity'] = weather['humidity']
    return df

→ RUN THIS FIRST! Easy +2% accuracy


Step 2: Economic Calendar (EASY - 2 giờ)
────────────────────────────────────────

def add_economic_features(df):
    df['is_payday_week'] = (df['date'].dt.day <= 7).astype(int)
    df['days_since_payday'] = (df['date'].dt.day - 1) % 30
    df['is_month_end'] = (df['date'].dt.day >= 25).astype(int)
    return df

→ RUN THIS SECOND! Easy +1% accuracy


Step 3: Social Events (MEDIUM - 1 tuần)
───────────────────────────────────────

# Manual calendar for now
HOLIDAYS_2025 = {
    '2025-01-28': 'Lunar New Year',
    '2025-04-30': 'Reunification Day',
    '2025-05-01': 'Labor Day',
    '2025-09-02': 'National Day'
}

def add_social_features(df):
    df['is_public_holiday'] = df['date'].astype(str).isin(HOLIDAYS_2025)
    # Add lunar calendar logic
    return df

→ DO THIS THIRD! Medium effort, good impact


Step 4: Test & Validate
───────────────────────

# Before
accuracy_before = test_model(features_17)
print(f"Before: {accuracy_before:.2%}")

# After  
accuracy_after = test_model(features_30)  # Added 13 features
print(f"After: {accuracy_after:.2%}")
print(f"Improvement: {accuracy_after - accuracy_before:.2%}")

Expected output:
Before: 92.3%
After: 94.8%
Improvement: +2.5%

→ WORTH IT!
""")
