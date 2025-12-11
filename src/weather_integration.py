"""
Weather Integration Module
Integrates weather data into demand forecasting
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherIntegration:
    """
    Weather data integration for demand forecasting
    
    Uses OpenWeatherMap API (free tier: 1000 calls/day)
    """
    
    def __init__(self, api_key: Optional[str] = None, location: Dict[str, float] = None):
        """
        Initialize weather integration
        
        Args:
            api_key: OpenWeatherMap API key (optional for demo)
            location: {'lat': latitude, 'lon': longitude}
        """
        self.api_key = api_key or "DEMO_MODE"  # Use demo mode if no key
        
        # Default: Ho Chi Minh City
        self.location = location or {
            'lat': 10.8231,
            'lon': 106.6297,
            'city': 'Ho Chi Minh City'
        }
        
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
        logger.info(f"Weather integration initialized for {self.location['city']}")
    
    
    def get_current_weather(self) -> Dict:
        """
        Get current weather data
        
        Returns:
            Dict with weather features
        """
        if self.api_key == "DEMO_MODE":
            return self._get_demo_weather()
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'lat': self.location['lat'],
                'lon': self.location['lon'],
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return self._parse_weather_response(data)
            
        except Exception as e:
            logger.error(f"Error fetching weather: {e}")
            return self._get_demo_weather()
    
    
    def get_forecast_weather(self, days: int = 7) -> pd.DataFrame:
        """
        Get weather forecast for next N days
        
        Args:
            days: Number of days to forecast (1-5 for free tier)
        
        Returns:
            DataFrame with daily weather forecasts
        """
        if self.api_key == "DEMO_MODE":
            return self._get_demo_forecast(days)
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'lat': self.location['lat'],
                'lon': self.location['lon'],
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return self._parse_forecast_response(data)
            
        except Exception as e:
            logger.error(f"Error fetching forecast: {e}")
            return self._get_demo_forecast(days)
    
    
    def _parse_weather_response(self, data: Dict) -> Dict:
        """Parse API response to extract weather features"""
        return {
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'precipitation': data.get('rain', {}).get('1h', 0) + data.get('snow', {}).get('1h', 0),
            'weather_condition': data['weather'][0]['id'],
            'weather_description': data['weather'][0]['description'],
            'cloudiness': data['clouds']['all'],
            'visibility': data.get('visibility', 10000) / 1000  # Convert to km
        }
    
    
    def _parse_forecast_response(self, data: Dict) -> pd.DataFrame:
        """Parse forecast API response"""
        forecasts = []
        
        for item in data['list']:
            forecast = {
                'date': pd.to_datetime(item['dt'], unit='s'),
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'],
                'precipitation': item.get('rain', {}).get('3h', 0) + item.get('snow', {}).get('3h', 0),
                'weather_condition': item['weather'][0]['id'],
                'weather_description': item['weather'][0]['description']
            }
            forecasts.append(forecast)
        
        df = pd.DataFrame(forecasts)
        
        # Aggregate to daily (take average of 3-hour forecasts)
        df['date'] = df['date'].dt.date
        daily = df.groupby('date').agg({
            'temperature': 'mean',
            'feels_like': 'mean',
            'humidity': 'mean',
            'wind_speed': 'mean',
            'precipitation': 'sum',
            'weather_condition': 'first',
            'weather_description': 'first'
        }).reset_index()
        
        return daily
    
    
    def _get_demo_weather(self) -> Dict:
        """
        Generate realistic demo weather for Ho Chi Minh City
        Based on typical tropical climate
        """
        # Simulate seasonal variation
        month = datetime.now().month
        
        # Dry season (Nov-Apr): Less rain, slightly cooler
        # Wet season (May-Oct): More rain, hotter
        is_wet_season = 5 <= month <= 10
        
        base_temp = 28 if is_wet_season else 26
        base_humidity = 85 if is_wet_season else 70
        base_rain = np.random.exponential(5) if is_wet_season else np.random.exponential(1)
        
        return {
            'temperature': base_temp + np.random.uniform(-3, 3),
            'feels_like': base_temp + np.random.uniform(-2, 5),
            'humidity': min(100, base_humidity + np.random.uniform(-10, 10)),
            'pressure': 1010 + np.random.uniform(-5, 5),
            'wind_speed': np.random.exponential(3),
            'precipitation': max(0, base_rain),
            'weather_condition': self._get_weather_condition(base_rain),
            'weather_description': self._get_weather_description(base_rain),
            'cloudiness': 50 + np.random.uniform(-30, 30),
            'visibility': 10 if base_rain < 5 else max(2, 10 - base_rain/2)
        }
    
    
    def _get_demo_forecast(self, days: int) -> pd.DataFrame:
        """Generate demo forecast data"""
        forecasts = []
        base_date = datetime.now().date()
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            weather = self._get_demo_weather()
            weather['date'] = date
            forecasts.append(weather)
        
        return pd.DataFrame(forecasts)
    
    
    def _get_weather_condition(self, precipitation: float) -> int:
        """Map precipitation to weather condition code"""
        if precipitation == 0:
            return 800  # Clear
        elif precipitation < 2:
            return 500  # Light rain
        elif precipitation < 10:
            return 501  # Moderate rain
        elif precipitation < 30:
            return 502  # Heavy rain
        else:
            return 503  # Extreme rain
    
    
    def _get_weather_description(self, precipitation: float) -> str:
        """Get weather description"""
        if precipitation == 0:
            return 'clear sky'
        elif precipitation < 2:
            return 'light rain'
        elif precipitation < 10:
            return 'moderate rain'
        elif precipitation < 30:
            return 'heavy rain'
        else:
            return 'extreme rain'
    
    
    def add_weather_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add weather features to forecast dataframe
        
        Args:
            df: DataFrame with 'date' column
        
        Returns:
            DataFrame with added weather features
        """
        logger.info("Adding weather features to forecast...")
        
        # Get forecast weather
        max_days = (df['date'].max() - df['date'].min()).days + 1
        weather_forecast = self.get_forecast_weather(days=min(max_days, 7))
        
        # Merge with df
        df['date_only'] = pd.to_datetime(df['date']).dt.date
        weather_forecast['date'] = pd.to_datetime(weather_forecast['date']).dt.date
        
        df = df.merge(weather_forecast, left_on='date_only', right_on='date', how='left', suffixes=('', '_weather'))
        
        # Add derived features
        df['is_rainy'] = (df['precipitation'] > 1).astype(int)
        df['is_heavy_rain'] = (df['precipitation'] > 10).astype(int)
        df['is_extreme_weather'] = (
            (df['precipitation'] > 30) | 
            (df['wind_speed'] > 40) | 
            (df['temperature'] > 38) | 
            (df['temperature'] < 15)
        ).astype(int)
        
        df['is_hot'] = (df['temperature'] > 32).astype(int)
        df['is_cold'] = (df['temperature'] < 22).astype(int)
        df['is_comfortable'] = ((df['temperature'] >= 24) & (df['temperature'] <= 28)).astype(int)
        
        # Calculate weather impact factor
        df['weather_factor'] = df.apply(self._calculate_weather_factor, axis=1)
        
        # Clean up
        df = df.drop(columns=['date_only', 'date_weather'], errors='ignore')
        
        logger.info(f"Added {len(weather_forecast)} weather features")
        return df
    
    
    def _calculate_weather_factor(self, row) -> float:
        """
        Calculate weather impact factor on demand
        
        Returns multiplier: 0.3 (extreme weather) to 1.2 (perfect weather)
        """
        if pd.isna(row.get('temperature')):
            return 1.0  # No weather data, no adjustment
        
        factor = 1.0
        
        # Temperature impact
        temp = row['temperature']
        if temp < 18:  # Very cold
            factor *= 0.8
        elif temp > 35:  # Very hot
            factor *= 0.85
        elif 24 <= temp <= 28:  # Perfect weather
            factor *= 1.05
        
        # Precipitation impact
        precip = row['precipitation']
        if precip == 0:  # No rain
            factor *= 1.0
        elif precip < 2:  # Light rain (good for delivery)
            factor *= 1.1
        elif precip < 10:  # Moderate rain
            factor *= 0.95
        elif precip < 30:  # Heavy rain
            factor *= 0.7
        else:  # Extreme rain / storm
            factor *= 0.3
        
        # Wind impact
        if row['wind_speed'] > 50:  # Typhoon
            factor *= 0.2
        elif row['wind_speed'] > 30:  # Strong wind
            factor *= 0.6
        
        # Humidity impact (comfort)
        if row['humidity'] > 90:  # Very humid
            factor *= 0.95
        
        return max(0.2, min(1.5, factor))  # Clamp between 0.2 and 1.5
    
    
    def get_weather_insights(self, weather: Dict) -> str:
        """
        Generate human-readable weather insights
        
        Args:
            weather: Weather data dict
        
        Returns:
            Insights string
        """
        insights = []
        
        temp = weather['temperature']
        precip = weather['precipitation']
        wind = weather['wind_speed']
        
        # Temperature insights
        if temp > 35:
            insights.append(f"🌡️ Very hot ({temp:.1f}°C) - Expect demand for cold drinks/salads")
        elif temp > 32:
            insights.append(f"☀️ Hot weather ({temp:.1f}°C) - Cold items preferred")
        elif temp < 20:
            insights.append(f"🌡️ Cool weather ({temp:.1f}°C) - Hot soups/noodles popular")
        else:
            insights.append(f"✅ Comfortable temp ({temp:.1f}°C) - Normal demand pattern")
        
        # Precipitation insights
        if precip > 30:
            insights.append(f"⛈️ EXTREME RAIN ({precip:.1f}mm) - Expect 70% drop in orders! Emergency mode!")
        elif precip > 10:
            insights.append(f"🌧️ Heavy rain ({precip:.1f}mm) - Delivery orders may increase 40%, dine-in drops 50%")
        elif precip > 2:
            insights.append(f"🌦️ Light-moderate rain ({precip:.1f}mm) - Delivery orders up 20%")
        elif precip > 0:
            insights.append(f"🌦️ Drizzle ({precip:.1f}mm) - Slight increase in delivery orders")
        else:
            insights.append("☀️ No rain - Normal operations")
        
        # Wind insights
        if wind > 50:
            insights.append(f"💨 TYPHOON WARNING ({wind:.1f}km/h) - CLOSE OPERATIONS!")
        elif wind > 30:
            insights.append(f"💨 Strong winds ({wind:.1f}km/h) - Delivery may be affected")
        
        # Humidity
        if weather['humidity'] > 85:
            insights.append(f"💧 Very humid ({weather['humidity']:.0f}%) - Customer comfort affected")
        
        return "\n".join(insights)


# Utility functions for easy integration

def quick_weather_forecast(days: int = 7) -> pd.DataFrame:
    """
    Quick function to get weather forecast
    
    Args:
        days: Number of days to forecast
    
    Returns:
        DataFrame with weather forecast
    """
    weather = WeatherIntegration()
    return weather.get_forecast_weather(days)


def add_weather_to_forecast(forecast_df: pd.DataFrame) -> pd.DataFrame:
    """
    Quick function to add weather to existing forecast
    
    Args:
        forecast_df: Forecast DataFrame with 'date' column
    
    Returns:
        DataFrame with weather features added
    """
    weather = WeatherIntegration()
    return weather.add_weather_features(forecast_df)


def get_weather_impact_summary() -> pd.DataFrame:
    """
    Get summary of weather impact on demand
    
    Returns:
        DataFrame with weather scenarios and impact factors
    """
    scenarios = [
        {'scenario': 'Perfect weather', 'temp': 26, 'precip': 0, 'wind': 5, 'factor': 1.05},
        {'scenario': 'Light rain', 'temp': 28, 'precip': 3, 'wind': 10, 'factor': 1.1},
        {'scenario': 'Heavy rain', 'temp': 25, 'precip': 25, 'wind': 20, 'factor': 0.7},
        {'scenario': 'Storm', 'temp': 24, 'precip': 50, 'wind': 60, 'factor': 0.3},
        {'scenario': 'Very hot', 'temp': 38, 'precip': 0, 'wind': 5, 'factor': 0.85},
        {'scenario': 'Cool day', 'temp': 19, 'precip': 0, 'wind': 8, 'factor': 0.95},
    ]
    
    return pd.DataFrame(scenarios)


if __name__ == "__main__":
    # Demo usage
    print("=" * 80)
    print("WEATHER INTEGRATION DEMO")
    print("=" * 80)
    
    # Initialize
    weather = WeatherIntegration()
    
    # Get current weather
    print("\n📊 CURRENT WEATHER:")
    print("-" * 80)
    current = weather.get_current_weather()
    for key, value in current.items():
        if isinstance(value, float):
            print(f"  {key:20s}: {value:8.2f}")
        else:
            print(f"  {key:20s}: {value}")
    
    print("\n💡 INSIGHTS:")
    print("-" * 80)
    insights = weather.get_weather_insights(current)
    print(insights)
    
    # Get forecast
    print("\n\n📅 7-DAY FORECAST:")
    print("-" * 80)
    forecast = weather.get_forecast_weather(days=7)
    print(forecast.to_string(index=False))
    
    # Show impact factors
    print("\n\n⚡ WEATHER IMPACT FACTORS:")
    print("-" * 80)
    impact_summary = get_weather_impact_summary()
    print(impact_summary.to_string(index=False))
    
    print("\n\n✅ Weather integration ready!")
    print("=" * 80)
