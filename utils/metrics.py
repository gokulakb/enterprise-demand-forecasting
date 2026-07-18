"""
Metrics calculation utilities
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Union
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import logging

logger = logging.getLogger(__name__)

class MetricsCalculator:
    """
    Calculate various metrics for forecasting and analysis
    """
    
    @staticmethod
    def calculate_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Absolute Percentage Error
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            MAPE value
        """
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
        # Remove NaN values
        mask = ~(np.isnan(y_true) | np.isnan(y_pred))
        y_true = y_true[mask]
        y_pred = y_pred[mask]
        
        if len(y_true) == 0 or len(y_pred) == 0:
            return np.nan
        
        mask = y_true != 0
        if not mask.any():
            return np.nan
        
        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    
    @staticmethod
    def calculate_accuracy_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """
        Calculate multiple accuracy metrics
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary with metrics
        """
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
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
        
        return {
            'MAE': mean_absolute_error(y_true, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'MAPE': MetricsCalculator.calculate_mape(y_true, y_pred),
            'R2': r2_score(y_true, y_pred)
        }
    
    @staticmethod
    def calculate_growth_rate(data: pd.Series, periods: int = 7) -> float:
        """
        Calculate growth rate over a period
        
        Args:
            data: Time series data
            periods: Number of periods for comparison
            
        Returns:
            Growth rate as percentage
        """
        if len(data) < periods * 2:
            return 0
        
        recent = data.iloc[-periods:].mean()
        previous = data.iloc[-periods*2:-periods].mean()
        
        if previous == 0:
            return 0
        
        return ((recent - previous) / previous) * 100
    
    @staticmethod
    def calculate_cagr(data: pd.Series) -> float:
        """
        Calculate Compound Annual Growth Rate
        
        Args:
            data: Time series data
            
        Returns:
            CAGR as percentage
        """
        if len(data) < 2:
            return 0
        
        start = data.iloc[0]
        end = data.iloc[-1]
        n = len(data)
        
        if start == 0 or n == 0:
            return 0
        
        return (np.power(end / start, 1 / n) - 1) * 100
    
    @staticmethod
    def calculate_seasonal_strength(data: pd.Series) -> float:
        """
        Calculate seasonal strength
        
        Args:
            data: Time series data
            
        Returns:
            Seasonal strength (0-1)
        """
        if len(data) < 14:  # Need at least 2 weeks
            return 0
        
        # Decompose using simple method
        from statsmodels.tsa.seasonal import seasonal_decompose
        try:
            decomposition = seasonal_decompose(data, model='additive', period=7)
            seasonal_var = decomposition.seasonal.var()
            residual_var = decomposition.resid.var()
            
            if seasonal_var + residual_var == 0:
                return 0
            
            return seasonal_var / (seasonal_var + residual_var)
        except Exception as e:
            logger.error(f"Seasonal strength calculation failed: {e}")
            return 0
    
    @staticmethod
    def calculate_forecast_confidence(metrics: Dict) -> float:
        """
        Calculate forecast confidence score
        
        Args:
            metrics: Dictionary with accuracy metrics
            
        Returns:
            Confidence score (0-100)
        """
        if not metrics:
            return 0
        
        # Extract metrics
        mape = metrics.get('MAPE', 100)
        r2 = metrics.get('R2', 0)
        
        # Calculate confidence based on MAPE and R²
        confidence = 0
        
        # MAPE contribution (up to 60%)
        if mape is not None and mape > 0:
            mape_score = max(0, min(60, 60 - mape * 0.6))
            confidence += mape_score
        
        # R² contribution (up to 40%)
        if r2 is not None:
            r2_score = max(0, min(40, r2 * 40))
            confidence += r2_score
        
        return confidence