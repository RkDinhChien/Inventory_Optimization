"""
Market Factors Integration
Economic, Social, Competition, and Marketing factors for demand forecasting
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MarketFactors:
    """
    Integrate market factors into demand forecasting:
    - Economic factors (payday, inflation, fuel prices)
    - Social factors (holidays, events, COVID restrictions)
    - Competition factors (nearby restaurants, promotions)
    - Marketing factors (our promotions, ads, social media)
    """
    
    def __init__(self, location: str = "Ho Chi Minh City"):
        self.location = location
        self._init_calendars()
        logger.info(f"Market factors initialized for {location}")
    
    
    def _init_calendars(self):
        """Initialize Vietnamese holiday and event calendars"""
        
        # Vietnamese Public Holidays 2025
        self.holidays_2025 = {
            '2025-01-01': 'New Year',
            '2025-01-28': 'Lunar New Year Eve',
            '2025-01-29': 'Lunar New Year (Tết) Day 1',
            '2025-01-30': 'Lunar New Year (Tết) Day 2',
            '2025-01-31': 'Lunar New Year (Tết) Day 3',
            '2025-02-01': 'Lunar New Year (Tết) Day 4',
            '2025-02-02': 'Lunar New Year (Tết) Day 5',
            '2025-04-10': 'Hung Kings Festival',
            '2025-04-30': 'Reunification Day',
            '2025-05-01': 'Labor Day',
            '2025-09-02': 'National Day',
            '2025-09-03': 'National Day Holiday'
        }
        
        # Major events
        self.major_events = {
            '2025-02-14': 'Valentine Day',
            '2025-03-08': 'Women Day',
            '2025-05-11': 'Mother Day',
            '2025-06-15': 'Father Day',
            '2025-10-20': 'Vietnamese Women Day',
            '2025-11-20': 'Teachers Day',
            '2025-12-24': 'Christmas Eve',
            '2025-12-25': 'Christmas'
        }
        
        # School calendar
        self.school_holidays = {
            'summer': [('2025-06-01', '2025-08-31')],
            'tet': [('2025-01-25', '2025-02-10')],
            'exam_weeks': [
                ('2025-01-02', '2025-01-15'),  # Semester 1 exams
                ('2025-05-15', '2025-05-30'),  # Semester 2 exams
                ('2025-12-15', '2025-12-30')   # Final exams
            ]
        }
    
    
    # ==================== ECONOMIC FACTORS ====================
    
    def get_economic_features(self, date: datetime) -> Dict:
        """
        Get economic factors for a specific date
        
        Returns:
            Dict with economic features
        """
        features = {}
        
        # Payday effects
        day = date.day
        features['is_payday_week'] = 1 if day <= 7 else 0
        features['days_since_payday'] = (day - 1) % 30
        features['is_month_end'] = 1 if day >= 25 else 0
        
        # Payday cycle factor
        if day <= 7:
            features['payday_factor'] = 1.3  # +30% spending
        elif day <= 15:
            features['payday_factor'] = 1.1  # +10% spending
        elif day <= 25:
            features['payday_factor'] = 1.0  # Normal
        else:
            features['payday_factor'] = 0.8  # -20% spending (end month)
        
        # Simulated economic indicators (in production, get from APIs)
        month = date.month
        features['inflation_rate'] = 3.5 + np.random.uniform(-0.5, 0.5)  # ~3.5%
        features['fuel_price'] = 22000 + np.random.uniform(-2000, 2000)  # VND/liter
        features['consumer_confidence'] = 85 + np.random.uniform(-10, 10)  # Index 0-100
        
        # Price sensitivity based on inflation
        if features['inflation_rate'] > 7:
            features['price_sensitivity'] = 0.85  # High inflation → reduce spending
        elif features['inflation_rate'] > 4:
            features['price_sensitivity'] = 0.95
        else:
            features['price_sensitivity'] = 1.0
        
        return features
    
    
    # ==================== SOCIAL FACTORS ====================
    
    def get_social_features(self, date: datetime) -> Dict:
        """
        Get social factors for a specific date
        
        Returns:
            Dict with social features
        """
        features = {}
        date_str = date.strftime('%Y-%m-%d')
        
        # Public holidays
        features['is_public_holiday'] = 1 if date_str in self.holidays_2025 else 0
        features['holiday_name'] = self.holidays_2025.get(date_str, None)
        
        # Lunar New Year (Tết) period
        tet_dates = [k for k in self.holidays_2025.keys() if 'Lunar New Year' in self.holidays_2025[k]]
        features['is_lunar_new_year'] = 1 if date_str in tet_dates else 0
        features['days_to_tet'] = self._days_to_date(date, '2025-01-29')
        
        # Major events
        features['is_major_event'] = 1 if date_str in self.major_events else 0
        features['event_name'] = self.major_events.get(date_str, None)
        
        # School calendar
        features['is_school_holiday'] = self._check_school_holiday(date)
        features['is_exam_week'] = self._check_exam_week(date)
        
        # Sports events (simulated - in production, use API)
        features['is_sports_event'] = self._check_sports_event(date)
        
        # COVID restrictions (simulated)
        features['covid_restriction_level'] = 0  # 0=none, 1-5=increasing restrictions
        
        # Social factor multiplier
        features['social_factor'] = self._calculate_social_factor(features)
        
        return features
    
    
    def _days_to_date(self, current_date: datetime, target_date_str: str) -> int:
        """Calculate days until target date"""
        target = datetime.strptime(target_date_str, '%Y-%m-%d')
        delta = (target - current_date).days
        return max(0, delta) if delta >= 0 else 365 + delta
    
    
    def _check_school_holiday(self, date: datetime) -> int:
        """Check if date is in school holiday period"""
        date_str = date.strftime('%Y-%m-%d')
        
        for period_type, periods in self.school_holidays.items():
            if period_type == 'exam_weeks':
                continue
            for start, end in periods:
                if start <= date_str <= end:
                    return 1
        return 0
    
    
    def _check_exam_week(self, date: datetime) -> int:
        """Check if date is in exam week"""
        date_str = date.strftime('%Y-%m-%d')
        
        for start, end in self.school_holidays['exam_weeks']:
            if start <= date_str <= end:
                return 1
        return 0
    
    
    def _check_sports_event(self, date: datetime) -> int:
        """Check if there's a major sports event (simulated)"""
        # In production, integrate with sports API
        # For demo, randomly assign some dates
        return 1 if date.day % 15 == 0 and date.weekday() in [5, 6] else 0
    
    
    def _calculate_social_factor(self, features: Dict) -> float:
        """
        Calculate overall social impact factor
        
        Returns multiplier: 0.2 (lockdown) to 5.0 (Tết)
        """
        factor = 1.0
        
        # Lunar New Year (Tết) - MASSIVE impact
        if features['is_lunar_new_year']:
            factor *= 5.0  # +400% demand!
        
        # Major holidays
        elif features['is_public_holiday']:
            if features['holiday_name'] in ['Reunification Day', 'Labor Day', 'National Day']:
                factor *= 2.0  # +100% major holidays
            else:
                factor *= 1.5  # +50% minor holidays
        
        # Special events
        elif features['is_major_event']:
            if features['event_name'] in ['Valentine Day', 'Christmas']:
                factor *= 1.8  # +80% romantic holidays
            else:
                factor *= 1.3  # +30% other events
        
        # Sports events
        if features['is_sports_event']:
            factor *= 1.4  # +40% during sports events
        
        # School holidays
        if features['is_school_holiday']:
            factor *= 1.2  # +20% families eating out
        
        # Exam weeks
        if features['is_exam_week']:
            factor *= 0.75  # -25% students busy studying
        
        # COVID restrictions
        if features['covid_restriction_level'] >= 4:
            factor *= 0.3  # -70% strict lockdown
        elif features['covid_restriction_level'] >= 2:
            factor *= 0.6  # -40% partial restrictions
        
        return factor
    
    
    # ==================== COMPETITION FACTORS ====================
    
    def get_competition_features(self, date: datetime) -> Dict:
        """
        Get competition factors
        
        In production, scrape competitor data from:
        - Google Maps API
        - Food delivery apps (Grab, ShopeeFood, GoFood)
        - Social media monitoring
        """
        features = {}
        
        # Simulated competition data
        features['num_competitors_nearby'] = np.random.randint(3, 8)  # 3-7 competitors
        features['avg_competitor_rating'] = 3.5 + np.random.uniform(0, 1)  # 3.5-4.5 stars
        features['competitor_promotion_active'] = np.random.choice([0, 1], p=[0.7, 0.3])  # 30% chance
        
        # Price comparison (our price vs average)
        our_price = 50000  # VND
        avg_competitor_price = 45000 + np.random.uniform(-5000, 10000)
        features['price_difference_pct'] = ((our_price - avg_competitor_price) / avg_competitor_price) * 100
        
        # New competitor opened recently
        features['new_competitor_opened'] = 1 if date.day == 1 else 0
        
        # Competition factor
        features['competition_factor'] = self._calculate_competition_factor(features)
        
        return features
    
    
    def _calculate_competition_factor(self, features: Dict) -> float:
        """Calculate competition impact factor"""
        factor = 1.0
        
        # Number of competitors
        num_comp = features['num_competitors_nearby']
        if num_comp <= 2:
            factor *= 1.3  # Low competition
        elif num_comp <= 5:
            factor *= 1.0  # Medium competition
        else:
            factor *= 0.85  # High competition
        
        # Competitor promotions
        if features['competitor_promotion_active']:
            factor *= 0.75  # -25% when competitors have promotions
        
        # New competitor impact
        if features['new_competitor_opened']:
            factor *= 0.85  # -15% initial impact
        
        # Price competitiveness
        price_diff = features['price_difference_pct']
        if price_diff > 20:  # We're 20% more expensive
            factor *= 0.8
        elif price_diff < -10:  # We're 10% cheaper
            factor *= 1.1
        
        return factor
    
    
    # ==================== MARKETING FACTORS ====================
    
    def get_marketing_features(self, date: datetime, 
                               has_promotion: bool = False,
                               discount_pct: float = 0,
                               ad_spend: float = 0) -> Dict:
        """
        Get marketing factors
        
        Args:
            date: Date to check
            has_promotion: Whether we're running a promotion
            discount_pct: Discount percentage (0-100)
            ad_spend: Daily ad spend in VND
        
        Returns:
            Dict with marketing features
        """
        features = {}
        
        # Promotion status
        features['has_promotion'] = 1 if has_promotion else 0
        features['discount_percentage'] = discount_pct
        
        # Marketing spend
        features['ad_spend'] = ad_spend
        features['has_active_ads'] = 1 if ad_spend > 0 else 0
        
        # Simulated marketing metrics
        if ad_spend > 0:
            features['ad_impressions'] = ad_spend / 10  # ~10 VND per impression
            features['ad_clicks'] = features['ad_impressions'] * 0.02  # 2% CTR
        else:
            features['ad_impressions'] = 0
            features['ad_clicks'] = 0
        
        # Social media metrics (simulated)
        features['social_media_mentions'] = np.random.randint(10, 100)
        features['viral_content_score'] = np.random.randint(0, 20)  # Rare to go viral
        
        # Email/SMS marketing
        features['email_campaign_active'] = 0  # Can be configured
        
        # Marketing factor
        features['marketing_factor'] = self._calculate_marketing_factor(features)
        
        return features
    
    
    def _calculate_marketing_factor(self, features: Dict) -> float:
        """Calculate marketing impact factor"""
        factor = 1.0
        
        # Promotion impact
        if features['has_promotion']:
            discount = features['discount_percentage']
            if discount >= 50:
                factor *= 2.5  # +150% for 50%+ discount
            elif discount >= 30:
                factor *= 1.8  # +80% for 30-49% discount
            elif discount >= 20:
                factor *= 1.5  # +50% for 20-29% discount
            elif discount >= 10:
                factor *= 1.3  # +30% for 10-19% discount
        
        # Advertising impact
        if features['ad_spend'] > 5000000:  # >5M VND
            factor *= 1.4  # +40% for heavy advertising
        elif features['ad_spend'] > 2000000:  # >2M VND
            factor *= 1.2  # +20% for medium advertising
        elif features['ad_spend'] > 0:
            factor *= 1.1  # +10% for light advertising
        
        # Viral content impact
        if features['viral_content_score'] > 80:
            factor *= 5.0  # +400% viral hit!
        elif features['viral_content_score'] > 50:
            factor *= 2.0  # +100% popular content
        
        return factor
    
    
    # ==================== COMBINED FEATURES ====================
    
    def add_all_market_features(self, df: pd.DataFrame,
                                has_promotion: bool = False,
                                discount_pct: float = 0,
                                ad_spend: float = 0) -> pd.DataFrame:
        """
        Add all market factors to forecast dataframe
        
        Args:
            df: DataFrame with 'date' column
            has_promotion: Promotion status
            discount_pct: Discount percentage
            ad_spend: Daily ad spend
        
        Returns:
            DataFrame with all market features added
        """
        logger.info("Adding market factors to forecast...")
        
        df['date_dt'] = pd.to_datetime(df['date'])
        
        # Collect all features
        all_features = []
        
        for idx, row in df.iterrows():
            date = row['date_dt']
            
            # Get all factor groups
            economic = self.get_economic_features(date)
            social = self.get_social_features(date)
            competition = self.get_competition_features(date)
            marketing = self.get_marketing_features(date, has_promotion, discount_pct, ad_spend)
            
            # Combine
            combined = {
                'date': date,
                **economic,
                **social,
                **competition,
                **marketing
            }
            
            all_features.append(combined)
        
        # Convert to dataframe
        features_df = pd.DataFrame(all_features)
        
        # Merge with original df
        df = df.merge(features_df, left_on='date_dt', right_on='date', how='left', suffixes=('', '_market'))
        
        # Calculate combined market factor
        df['market_factor'] = (
            df['payday_factor'] * 
            df['social_factor'] * 
            df['competition_factor'] * 
            df['marketing_factor'] *
            df['price_sensitivity']
        )
        
        # Clean up
        df = df.drop(columns=['date_dt', 'date_market'], errors='ignore')
        
        logger.info(f"Added {len(features_df.columns)} market features")
        
        return df
    
    
    def get_market_insights(self, features: Dict) -> List[str]:
        """Generate human-readable insights from market features"""
        insights = []
        
        # Economic insights
        if features['is_payday_week']:
            insights.append(f"💰 Payday week - Expect +30% spending")
        elif features['is_month_end']:
            insights.append(f"📉 End of month - Expect -20% spending")
        
        if features['inflation_rate'] > 5:
            insights.append(f"⚠️ High inflation ({features['inflation_rate']:.1f}%) - Price sensitive customers")
        
        # Social insights
        if features.get('is_lunar_new_year'):
            insights.append(f"🎊 TẾT - MASSIVE demand spike (+400%)! Prepare 5x inventory!")
        elif features.get('is_public_holiday'):
            insights.append(f"🎉 {features['holiday_name']} - Expect +50-100% demand")
        elif features.get('is_major_event'):
            insights.append(f"💝 {features['event_name']} - Expect +30-80% demand")
        
        if features.get('is_exam_week'):
            insights.append(f"📚 Exam week - Student orders down 25%")
        
        # Competition insights
        if features.get('competitor_promotion_active'):
            insights.append(f"🏷️ Competitor running promotion - May lose 25% customers")
        
        if features.get('price_difference_pct', 0) > 15:
            insights.append(f"💸 Our price {features['price_difference_pct']:.0f}% higher than competitors")
        
        # Marketing insights
        if features.get('has_promotion'):
            discount = features['discount_percentage']
            insights.append(f"🎁 {discount:.0f}% discount active - Expect +{(discount*2):.0f}-{(discount*3):.0f}% orders")
        
        if features.get('ad_spend', 0) > 2000000:
            insights.append(f"📢 Heavy advertising (₫{features['ad_spend']/1000000:.1f}M) - Expect +20-40% reach")
        
        return insights


# Utility functions

def quick_market_analysis(date: datetime) -> Dict:
    """Quick function to get all market factors for a date"""
    market = MarketFactors()
    
    economic = market.get_economic_features(date)
    social = market.get_social_features(date)
    competition = market.get_competition_features(date)
    marketing = market.get_marketing_features(date)
    
    return {
        'date': date,
        'economic': economic,
        'social': social,
        'competition': competition,
        'marketing': marketing
    }


def add_market_to_forecast(forecast_df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """Quick function to add market factors to forecast"""
    market = MarketFactors()
    return market.add_all_market_features(forecast_df, **kwargs)


if __name__ == "__main__":
    # Demo usage
    print("=" * 80)
    print("MARKET FACTORS INTEGRATION DEMO")
    print("=" * 80)
    
    market = MarketFactors()
    
    # Test specific dates
    test_dates = [
        datetime(2025, 1, 5),   # Payday week
        datetime(2025, 1, 29),  # Tết
        datetime(2025, 2, 14),  # Valentine
        datetime(2025, 12, 25), # End month
    ]
    
    for date in test_dates:
        print(f"\n{'='*80}")
        print(f"📅 DATE: {date.strftime('%A, %B %d, %Y')}")
        print("=" * 80)
        
        # Get all factors
        economic = market.get_economic_features(date)
        social = market.get_social_features(date)
        competition = market.get_competition_features(date)
        marketing = market.get_marketing_features(date, has_promotion=False)
        
        # Combine for insights
        all_features = {**economic, **social, **competition, **marketing}
        
        print(f"\n📊 FACTORS:")
        print(f"  Economic Factor:     {economic['payday_factor']:.2f}x")
        print(f"  Social Factor:       {social['social_factor']:.2f}x")
        print(f"  Competition Factor:  {competition['competition_factor']:.2f}x")
        print(f"  Marketing Factor:    {marketing['marketing_factor']:.2f}x")
        print(f"  Price Sensitivity:   {economic['price_sensitivity']:.2f}x")
        
        combined = (economic['payday_factor'] * social['social_factor'] * 
                   competition['competition_factor'] * marketing['marketing_factor'] *
                   economic['price_sensitivity'])
        print(f"\n  🎯 COMBINED FACTOR:  {combined:.2f}x")
        
        # Show insights
        insights = market.get_market_insights(all_features)
        if insights:
            print(f"\n💡 INSIGHTS:")
            for insight in insights:
                print(f"  {insight}")
        
        # Example calculation
        base_demand = 100
        adjusted_demand = base_demand * combined
        print(f"\n📈 IMPACT:")
        print(f"  Base demand:      {base_demand} servings")
        print(f"  Adjusted demand:  {adjusted_demand:.0f} servings")
        print(f"  Change:           {adjusted_demand - base_demand:+.0f} servings ({(combined-1)*100:+.1f}%)")
    
    print("\n" + "=" * 80)
    print("✅ Market factors integration ready!")
    print("=" * 80)
