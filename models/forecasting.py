"""
Demand forecasting module using multiple models
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from datetime import datetime, timedelta
import logging
import warnings
warnings.filterwarnings('ignore')

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
import pickle
import os

logger = logging.getLogger(__name__)

class DemandForecaster:
    """
    Enterprise demand forecasting with multiple models
    """
    
    def __init__(self):
        """Initialize the forecaster"""
        self.models = {}
        self.forecast_results = {}
        self.metrics = {}
        self.history = {}
        
    def prepare_data(self, df: pd.DataFrame, target_col: str, 
                     date_col: str = 'Date') -> pd.DataFrame:
        """
        Prepare time series data for forecasting
        
        Args:
            df: Input dataframe
            target_col: Column to forecast
            date_col: Date column name
            
        Returns:
            Prepared dataframe
        """
        data = df.copy()
        data[date_col] = pd.to_datetime(data[date_col])
        data = data.sort_values(date_col)
        data = data.set_index(date_col)
        data = data.asfreq('D')
        data[target_col] = data[target_col].interpolate()
        
        return data[[target_col]]
    
    def fit_moving_average(self, data: pd.DataFrame, window: int = 7) -> np.ndarray:
        """
        Fit moving average model
        
        Args:
            data: Time series data
            window: Window size for moving average
            
        Returns:
            Fitted values
        """
        return data.rolling(window=window, min_periods=1).mean().values.flatten()
    
    def fit_linear_regression(self, data: pd.DataFrame) -> Tuple:
        """
        Fit linear regression model
        
        Args:
            data: Time series data
            
        Returns:
            Model and predictions
        """
        X = np.arange(len(data)).reshape(-1, 1)
        y = data.values.flatten()
        
        model = LinearRegression()
        model.fit(X, y)
        predictions = model.predict(X)
        
        return model, predictions
    
    def fit_arima(self, data: pd.Series, order: Tuple = (5, 1, 0)) -> Tuple:
        """
        Fit ARIMA model
        
        Args:
            data: Time series data
            order: ARIMA order (p, d, q)
            
        Returns:
            Model and predictions
        """
        try:
            model = ARIMA(data, order=order)
            fitted = model.fit()
            predictions = fitted.fittedvalues
            return fitted, predictions
        except Exception as e:
            logger.error(f"ARIMA fitting failed: {e}")
            return None, None
    
    def fit_exponential_smoothing(self, data: pd.Series, 
                                  seasonal_periods: int = 7) -> Tuple:
        """
        Fit exponential smoothing model
        
        Args:
            data: Time series data
            seasonal_periods: Number of seasonal periods
            
        Returns:
            Model and predictions
        """
        try:
            model = ExponentialSmoothing(data, 
                                        seasonal_periods=seasonal_periods, 
                                        trend='add', 
                                        seasonal='add')
            fitted = model.fit()
            predictions = fitted.fittedvalues
            return fitted, predictions
        except Exception as e:
            logger.error(f"Exponential smoothing fitting failed: {e}")
            return None, None
    
    def forecast_with_prophet(self, df: pd.DataFrame, 
                             target_col: str, 
                             periods: int = 30) -> Optional[pd.DataFrame]:
        """
        Forecast using Prophet
        
        Args:
            df: Input dataframe with date and target
            target_col: Column to forecast
            periods: Number of periods to forecast
            
        Returns:
            Forecast dataframe
        """
        try:
            from prophet import Prophet
            
            # Prepare data for Prophet
            prophet_df = df.copy()
            prophet_df = prophet_df.reset_index()
            prophet_df['ds'] = pd.to_datetime(prophet_df['Date'])
            prophet_df['y'] = prophet_df[target_col]
            
            # Create and fit model
            model = Prophet(yearly_seasonality=True, 
                           weekly_seasonality=True,
                           daily_seasonality=False)
            model.fit(prophet_df[['ds', 'y']])
            
            # Make future dataframe
            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)
            
            return forecast
        except ImportError:
            logger.warning("Prophet not installed, using fallback")
            return None
        except Exception as e:
            logger.error(f"Prophet forecasting failed: {e}")
            return None
    
    def evaluate_model(self, y_true: np.ndarray, 
                       y_pred: np.ndarray) -> Dict:
        """
        Evaluate forecast accuracy
        
        Args:
            y_true: Actual values
            y_pred: Predicted values
            
        Returns:
            Dictionary of metrics
        """
        # Remove NaN values
        mask = ~(np.isnan(y_true) | np.isnan(y_pred))
        y_true = y_true[mask]
        y_pred = y_pred[mask]
        
        if len(y_true) == 0 or len(y_pred) == 0:
            return {
                'MAE': np.nan,
                'RMSE': np.nan,
                'MAPE': np.nan,
                'R2': np.nan
            }
        
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        
        # MAPE calculation
        mask = y_true != 0
        if mask.any():
            mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
        else:
            mape = np.nan
        
        return {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape,
            'R2': r2
        }
    
    def forecast(self, data: pd.DataFrame, target_col: str, 
                forecast_horizon: int = 90) -> Dict:
        """
        Generate comprehensive forecast
        
        Args:
            data: Input data
            target_col: Column to forecast
            forecast_horizon: Number of days to forecast
            
        Returns:
            Dictionary with forecast results
        """
        # Prepare data
        prepared_data = self.prepare_data(data, target_col)
        train_size = int(len(prepared_data) * 0.8)
        train = prepared_data.iloc[:train_size]
        test = prepared_data.iloc[train_size:]
        
        results = {
            'train': train,
            'test': test,
            'forecasts': {},
            'metrics': {},
            'forecast_values': None,
            'forecast_dates': None
        }
        
        # Fit models
        models = {
            'Moving Average': self.fit_moving_average(train),
            'Linear Regression': self.fit_linear_regression(train)[1],
            'ARIMA': self.fit_arima(train.values.flatten())[1],
            'Exponential Smoothing': self.fit_exponential_smoothing(train.values.flatten())[1]
        }
        
        # Evaluate on test set
        for name, predictions in models.items():
            if predictions is not None:
                if len(predictions) > 0:
                    # Align predictions with test data
                    test_pred = predictions[-len(test):] if len(predictions) >= len(test) else predictions
                    if len(test_pred) > 0 and len(test) > 0:
                        metrics = self.evaluate_model(
                            test.values.flatten()[:len(test_pred)], 
                            test_pred
                        )
                        results['metrics'][name] = metrics
        
        # Generate forecasts for future
        forecast_methods = {
            'ARIMA': self._forecast_arima,
            'Exponential Smoothing': self._forecast_exponential,
            'Prophet': self._forecast_prophet
        }
        
        forecast_values = []
        for name, method in forecast_methods.items():
            try:
                pred = method(train, forecast_horizon)
                if pred is not None and len(pred) > 0:
                    results['forecasts'][name] = pred
                    forecast_values.append(pred)
            except Exception as e:
                logger.error(f"Error with {name}: {e}")
                continue
        
        # Ensemble forecast (average of all models)
        if forecast_values:
            ensemble = np.mean(forecast_values, axis=0)
            results['forecasts']['Ensemble'] = ensemble
            results['forecast_values'] = ensemble
            
            # Generate forecast dates
            last_date = train.index[-1]
            forecast_dates = pd.date_range(start=last_date + timedelta(days=1), 
                                         periods=forecast_horizon, 
                                         freq='D')
            results['forecast_dates'] = forecast_dates
        
        # Store results
        self.forecast_results[target_col] = results
        self.history[target_col] = prepared_data
        
        return results
    
    def _forecast_arima(self, train: pd.DataFrame, horizon: int) -> Optional[np.ndarray]:
        """Generate ARIMA forecast"""
        try:
            model = ARIMA(train.values.flatten(), order=(5, 1, 0))
            fitted = model.fit()
            forecast = fitted.forecast(steps=horizon)
            return forecast.values
        except Exception as e:
            logger.error(f"ARIMA forecast failed: {e}")
            return None
    
    def _forecast_exponential(self, train: pd.DataFrame, horizon: int) -> Optional[np.ndarray]:
        """Generate exponential smoothing forecast"""
        try:
            model = ExponentialSmoothing(train.values.flatten(), 
                                        seasonal_periods=7, 
                                        trend='add', 
                                        seasonal='add')
            fitted = model.fit()
            forecast = fitted.forecast(steps=horizon)
            return forecast
        except Exception as e:
            logger.error(f"Exponential smoothing forecast failed: {e}")
            return None
    
    def _forecast_prophet(self, train: pd.DataFrame, horizon: int) -> Optional[np.ndarray]:
        """Generate Prophet forecast"""
        try:
            from prophet import Prophet
            
            prophet_df = train.reset_index()
            prophet_df.columns = ['ds', 'y']
            
            model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
            model.fit(prophet_df)
            
            future = model.make_future_dataframe(periods=horizon)
            forecast = model.predict(future)
            
            return forecast['yhat'].values[-horizon:]
        except Exception as e:
            logger.error(f"Prophet forecast failed: {e}")
            return None
    
    def get_forecast_accuracy(self, target_col: str) -> Dict:
        """
        Get forecast accuracy metrics
        
        Args:
            target_col: Target column name
            
        Returns:
            Dictionary of accuracy metrics
        """
        if target_col not in self.forecast_results:
            return {}
        
        results = self.forecast_results[target_col]
        return results.get('metrics', {})
    
    def get_seasonality(self, data: pd.DataFrame, target_col: str) -> Dict:
        """
        Detect seasonality in the data
        
        Args:
            data: Input data
            target_col: Target column
            
        Returns:
            Dictionary with seasonality information
        """
        prepared = self.prepare_data(data, target_col)
        
        try:
            # Decompose the series
            decomposition = seasonal_decompose(prepared[target_col], 
                                              model='additive', 
                                              period=7)
            
            return {
                'trend': decomposition.trend.values,
                'seasonal': decomposition.seasonal.values,
                'residual': decomposition.resid.values,
                'observed': decomposition.observed.values
            }
        except Exception as e:
            logger.error(f"Seasonality detection failed: {e}")
            return {}
    
    def detect_peaks(self, data: pd.Series, threshold: float = 1.5) -> pd.Series:
        """
        Detect peaks in time series data
        
        Args:
            data: Time series data
            threshold: Threshold for peak detection
            
        Returns:
            Boolean series indicating peaks
        """
        if isinstance(data, pd.DataFrame):
            data = data.iloc[:, 0]
        
        # Calculate rolling statistics
        rolling_mean = data.rolling(window=7, center=True).mean()
        rolling_std = data.rolling(window=7, center=True).std()
        
        # Detect peaks
        peaks = (data > rolling_mean + threshold * rolling_std)
        
        return peaks
    
    def save_model(self, filename: str) -> None:
        """Save the trained models"""
        with open(filename, 'wb') as f:
            pickle.dump(self.models, f)
        logger.info(f"Model saved to {filename}")
    
    def load_model(self, filename: str) -> None:
        """Load trained models"""
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.models = pickle.load(f)
            logger.info(f"Model loaded from {filename}")
        else:
            logger.warning(f"Model file {filename} not found")