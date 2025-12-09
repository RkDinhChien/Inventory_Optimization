"""
Machine Learning Forecaster Module for Inventory Optimization
Uses advanced ML algorithms: SARIMA, XGBoost, and Prophet
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# ML Libraries
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("Warning: Prophet not available. Install with: pip install prophet")


class MLForecaster:
    """
    Advanced Machine Learning forecaster for demand prediction.
    Supports multiple algorithms: SARIMA, XGBoost, Random Forest, and Prophet.
    """
    
    def __init__(self, algorithm: str = 'sarima'):
        """
        Initialize ML Forecaster.
        
        Args:
            algorithm: 'sarima', 'xgboost', 'random_forest', or 'prophet'
        """
        self.algorithm = algorithm.lower()
        self.models = {}
        self.label_encoder = LabelEncoder()
        self.is_fitted = False
        
        # Validate algorithm choice
        valid_algorithms = ['sarima', 'xgboost', 'random_forest', 'prophet']
        if self.algorithm not in valid_algorithms:
            raise ValueError(f"Algorithm must be one of {valid_algorithms}")
            
        if self.algorithm == 'prophet' and not PROPHET_AVAILABLE:
            raise ImportError("Prophet not installed. Please install: pip install prophet")
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare time-based features for ML models.
        
        Args:
            df: DataFrame with 'date' column
            
        Returns:
            DataFrame with engineered features
        """
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])
        
        # Time-based features
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_year'] = df['date'].dt.dayofyear
        df['week_of_year'] = df['date'].dt.isocalendar().week
        df['quarter'] = df['date'].dt.quarter
        
        # Cyclical features (sin/cos encoding for periodicity)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        df['day_of_week_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['day_of_week_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        # Boolean features
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['is_month_start'] = df['date'].dt.is_month_start.astype(int)
        df['is_month_end'] = df['date'].dt.is_month_end.astype(int)
        
        # Seasonal indicators
        df['is_winter'] = df['month'].isin([12, 1, 2]).astype(int)
        df['is_summer'] = df['month'].isin([6, 7, 8]).astype(int)
        df['is_spring'] = df['month'].isin([3, 4, 5]).astype(int)
        df['is_fall'] = df['month'].isin([9, 10, 11]).astype(int)
        
        return df
    
    def fit_sarima(self, dish_data: pd.DataFrame, dish_name: str) -> None:
        """
        Fit SARIMA model for a specific dish.
        SARIMA: Seasonal AutoRegressive Integrated Moving Average
        Best for: Time series with clear seasonal patterns
        
        Args:
            dish_data: Historical data for one dish
            dish_name: Name of the dish
        """
        try:
            # Prepare time series
            ts_data = dish_data.set_index('date')['quantity_sold']
            ts_data = ts_data.asfreq('D', fill_value=0)
            
            # SARIMA parameters (p,d,q) x (P,D,Q,s)
            # p,d,q: non-seasonal parameters (AR, I, MA)
            # P,D,Q,s: seasonal parameters with period s=7 (weekly)
            order = (1, 1, 1)  # Non-seasonal: AR(1), I(1), MA(1)
            seasonal_order = (1, 1, 1, 7)  # Seasonal: weekly pattern
            
            model = SARIMAX(
                ts_data,
                order=order,
                seasonal_order=seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            
            self.models[dish_name] = model.fit(disp=False, maxiter=200)
            print(f"✓ SARIMA model fitted for {dish_name}")
            
        except Exception as e:
            print(f"✗ Error fitting SARIMA for {dish_name}: {str(e)}")
            # Fallback to simple average
            self.models[dish_name] = {'type': 'average', 'value': dish_data['quantity_sold'].mean()}
    
    def fit_xgboost(self, dish_data: pd.DataFrame, dish_name: str) -> None:
        """
        Fit XGBoost model for a specific dish.
        XGBoost: Extreme Gradient Boosting
        Best for: Complex non-linear patterns and feature interactions
        
        Args:
            dish_data: Historical data for one dish
            dish_name: Name of the dish
        """
        try:
            # Prepare features
            df_features = self.prepare_features(dish_data)
            
            # Select features for training
            feature_cols = [
                'month', 'day_of_week', 'day_of_year', 'week_of_year', 'quarter',
                'month_sin', 'month_cos', 'day_of_week_sin', 'day_of_week_cos',
                'is_weekend', 'is_winter', 'is_summer', 'is_spring', 'is_fall'
            ]
            
            X = df_features[feature_cols]
            y = df_features['quantity_sold']
            
            # XGBoost with optimized parameters
            model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                objective='reg:squarederror'
            )
            
            model.fit(X, y)
            self.models[dish_name] = {'model': model, 'features': feature_cols}
            print(f"✓ XGBoost model fitted for {dish_name}")
            
        except Exception as e:
            print(f"✗ Error fitting XGBoost for {dish_name}: {str(e)}")
            self.models[dish_name] = {'type': 'average', 'value': dish_data['quantity_sold'].mean()}
    
    def fit_random_forest(self, dish_data: pd.DataFrame, dish_name: str) -> None:
        """
        Fit Random Forest model for a specific dish.
        Random Forest: Ensemble of decision trees
        Best for: Robust predictions with automatic feature importance
        
        Args:
            dish_data: Historical data for one dish
            dish_name: Name of the dish
        """
        try:
            # Prepare features
            df_features = self.prepare_features(dish_data)
            
            feature_cols = [
                'month', 'day_of_week', 'day_of_year', 'week_of_year', 'quarter',
                'month_sin', 'month_cos', 'day_of_week_sin', 'day_of_week_cos',
                'is_weekend', 'is_winter', 'is_summer', 'is_spring', 'is_fall'
            ]
            
            X = df_features[feature_cols]
            y = df_features['quantity_sold']
            
            # Random Forest with optimized parameters
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            model.fit(X, y)
            self.models[dish_name] = {'model': model, 'features': feature_cols}
            print(f"✓ Random Forest model fitted for {dish_name}")
            
        except Exception as e:
            print(f"✗ Error fitting Random Forest for {dish_name}: {str(e)}")
            self.models[dish_name] = {'type': 'average', 'value': dish_data['quantity_sold'].mean()}
    
    def fit_prophet(self, dish_data: pd.DataFrame, dish_name: str) -> None:
        """
        Fit Prophet model for a specific dish.
        Prophet: Facebook's forecasting tool
        Best for: Daily data with strong seasonal effects and holidays
        
        Args:
            dish_data: Historical data for one dish
            dish_name: Name of the dish
        """
        try:
            # Prophet requires specific column names: 'ds' and 'y'
            df_prophet = dish_data[['date', 'quantity_sold']].copy()
            df_prophet.columns = ['ds', 'y']
            
            # Initialize Prophet with seasonality
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                seasonality_mode='multiplicative',
                changepoint_prior_scale=0.05
            )
            
            model.fit(df_prophet)
            self.models[dish_name] = model
            print(f"✓ Prophet model fitted for {dish_name}")
            
        except Exception as e:
            print(f"✗ Error fitting Prophet for {dish_name}: {str(e)}")
            self.models[dish_name] = {'type': 'average', 'value': dish_data['quantity_sold'].mean()}
    
    def fit(self, orders_data: pd.DataFrame) -> None:
        """
        Train models for all dishes in the dataset.
        
        Args:
            orders_data: Historical orders DataFrame with columns:
                        ['date', 'dish_name', 'quantity_sold']
        """
        print(f"\n🤖 Training {self.algorithm.upper()} models...")
        print("=" * 60)
        
        orders_data['date'] = pd.to_datetime(orders_data['date'])
        
        # Train a model for each dish
        for dish_name in orders_data['dish_name'].unique():
            dish_data = orders_data[orders_data['dish_name'] == dish_name].copy()
            dish_data = dish_data.sort_values('date')
            
            # Select appropriate fitting method
            if self.algorithm == 'sarima':
                self.fit_sarima(dish_data, dish_name)
            elif self.algorithm == 'xgboost':
                self.fit_xgboost(dish_data, dish_name)
            elif self.algorithm == 'random_forest':
                self.fit_random_forest(dish_data, dish_name)
            elif self.algorithm == 'prophet':
                self.fit_prophet(dish_data, dish_name)
        
        self.is_fitted = True
        print("=" * 60)
        print(f"✅ All models trained successfully!\n")
    
    def predict(self, days_ahead: int = 7) -> pd.DataFrame:
        """
        Generate predictions for the next N days.
        
        Args:
            days_ahead: Number of days to forecast
            
        Returns:
            DataFrame with predictions
        """
        if not self.is_fitted:
            raise ValueError("Models not fitted. Call fit() first.")
        
        # Generate future dates
        start_date = datetime.now().date()
        future_dates = [start_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
        
        predictions = []
        
        for dish_name, model in self.models.items():
            for date in future_dates:
                # Get prediction based on algorithm
                if self.algorithm == 'sarima':
                    pred_value = self._predict_sarima(model, len(future_dates))
                elif self.algorithm in ['xgboost', 'random_forest']:
                    pred_value = self._predict_tree_model(model, date)
                elif self.algorithm == 'prophet':
                    pred_value = self._predict_prophet(model, date)
                else:
                    pred_value = model.get('value', 0)
                
                predictions.append({
                    'date': date,
                    'dish_name': dish_name,
                    'predicted_quantity': max(0, int(pred_value)),
                    'algorithm': self.algorithm
                })
        
        return pd.DataFrame(predictions)
    
    def _predict_sarima(self, model, steps: int) -> float:
        """Get SARIMA prediction."""
        try:
            if isinstance(model, dict) and model.get('type') == 'average':
                return model['value']
            forecast = model.forecast(steps=steps)
            return forecast.iloc[-1]
        except:
            return 0
    
    def _predict_tree_model(self, model_dict: dict, date) -> float:
        """Get XGBoost/Random Forest prediction."""
        try:
            if isinstance(model_dict, dict) and model_dict.get('type') == 'average':
                return model_dict['value']
            
            # Prepare features for prediction
            df_future = pd.DataFrame({'date': [date]})
            df_future = self.prepare_features(df_future)
            
            X = df_future[model_dict['features']]
            prediction = model_dict['model'].predict(X)
            return prediction[0]
        except:
            return 0
    
    def _predict_prophet(self, model, date) -> float:
        """Get Prophet prediction."""
        try:
            if isinstance(model, dict) and model.get('type') == 'average':
                return model['value']
            
            future = pd.DataFrame({'ds': [pd.Timestamp(date)]})
            forecast = model.predict(future)
            return forecast['yhat'].iloc[0]
        except:
            return 0
    
    def get_model_info(self) -> Dict:
        """
        Get information about the trained models.
        
        Returns:
            Dictionary with model information
        """
        info = {
            'algorithm': self.algorithm,
            'num_models': len(self.models),
            'dishes': list(self.models.keys()),
            'is_fitted': self.is_fitted
        }
        
        # Add algorithm-specific info
        if self.algorithm == 'sarima':
            info['description'] = 'SARIMA - Seasonal AutoRegressive Integrated Moving Average'
            info['best_for'] = 'Time series with seasonal patterns'
        elif self.algorithm == 'xgboost':
            info['description'] = 'XGBoost - Extreme Gradient Boosting'
            info['best_for'] = 'Complex non-linear patterns'
        elif self.algorithm == 'random_forest':
            info['description'] = 'Random Forest - Ensemble of Decision Trees'
            info['best_for'] = 'Robust predictions with feature importance'
        elif self.algorithm == 'prophet':
            info['description'] = 'Prophet - Facebook\'s Forecasting Tool'
            info['best_for'] = 'Daily data with holidays and seasonality'
        
        return info
