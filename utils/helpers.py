"""
Helper utility functions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import hashlib
import json
import logging

logger = logging.getLogger(__name__)

class Helpers:
    """
    Collection of helper functions
    """
    
    @staticmethod
    def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean a dataframe by handling missing values and formatting
        
        Args:
            df: Input dataframe
            
        Returns:
            Cleaned dataframe
        """
        df = df.copy()
        
        # Remove duplicate rows
        df = df.drop_duplicates()
        
        # Handle missing values
        for col in df.columns:
            if df[col].dtype in ['float64', 'int64']:
                df[col] = df[col].fillna(df[col].mean())
            elif df[col].dtype == 'object':
                df[col] = df[col].fillna('Unknown')
        
        # Convert date columns
        for col in df.columns:
            if 'date' in col.lower() or 'month' in col.lower() or 'day' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass
        
        return df
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """
        Format a number as currency
        
        Args:
            amount: Number to format
            
        Returns:
            Formatted currency string
        """
        return f"${amount:,.2f}"
    
    @staticmethod
    def format_percentage(value: float, decimals: int = 1) -> str:
        """
        Format a number as percentage
        
        Args:
            value: Number to format
            decimals: Number of decimal places
            
        Returns:
            Formatted percentage string
        """
        return f"{value:.{decimals}f}%"
    
    @staticmethod
    def format_number(value: float) -> str:
        """
        Format a number with appropriate suffix (K, M, B)
        
        Args:
            value: Number to format
            
        Returns:
            Formatted number string
        """
        if value >= 1_000_000_000:
            return f"{value/1_000_000_000:.1f}B"
        elif value >= 1_000_000:
            return f"{value/1_000_000:.1f}M"
        elif value >= 1_000:
            return f"{value/1_000:.1f}K"
        else:
            return f"{value:.0f}"
    
    @staticmethod
    def safe_divide(numerator: float, denominator: float, default: float = 0) -> float:
        """
        Safe division handling division by zero
        
        Args:
            numerator: Numerator
            denominator: Denominator
            default: Default value if denominator is zero
            
        Returns:
            Division result or default
        """
        if denominator == 0:
            return default
        return numerator / denominator
    
    @staticmethod
    def generate_summary_stats(df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics for a dataframe
        
        Args:
            df: Input dataframe
            
        Returns:
            Dictionary with summary statistics
        """
        stats = {
            'rows': len(df),
            'columns': len(df.columns),
            'missing_values': df.isnull().sum().sum(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024 ** 2  # MB
        }
        
        # Numeric columns
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        
        for col in numeric_cols:
            stats[f'{col}_mean'] = df[col].mean()
            stats[f'{col}_std'] = df[col].std()
            stats[f'{col}_min'] = df[col].min()
            stats[f'{col}_max'] = df[col].max()
        
        return stats
    
    @staticmethod
    def create_date_range(start_date: str, end_date: str, 
                         freq: str = 'D') -> List[datetime]:
        """
        Create a date range
        
        Args:
            start_date: Start date string
            end_date: End date string
            freq: Frequency (D, W, M)
            
        Returns:
            List of datetime objects
        """
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        return pd.date_range(start=start, end=end, freq=freq).tolist()
    
    @staticmethod
    def hash_string(text: str) -> str:
        """
        Generate hash of a string
        
        Args:
            text: Input text
            
        Returns:
            Hash string
        """
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
        """
        Split a list into chunks
        
        Args:
            lst: List to split
            chunk_size: Size of each chunk
            
        Returns:
            List of chunks
        """
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    
    @staticmethod
    def convert_timedelta_to_hours(td: pd.Timedelta) -> float:
        """
        Convert timedelta to hours
        
        Args:
            td: Timedelta object
            
        Returns:
            Hours as float
        """
        return td.total_seconds() / 3600
    
    @staticmethod
    def get_week_number(date: datetime) -> int:
        """
        Get ISO week number
        
        Args:
            date: Datetime object
            
        Returns:
            Week number
        """
        return date.isocalendar()[1]
    
    @staticmethod
    def is_weekend(date: datetime) -> bool:
        """
        Check if a date is on the weekend
        
        Args:
            date: Datetime object
            
        Returns:
            True if weekend, False otherwise
        """
        return date.weekday() >= 5
    
    @staticmethod
    def get_quarter(date: datetime) -> int:
        """
        Get quarter of the year
        
        Args:
            date: Datetime object
            
        Returns:
            Quarter number (1-4)
        """
        return (date.month - 1) // 3 + 1
    
    @staticmethod
    def calculate_confidence_interval(data: np.ndarray, confidence: float = 0.95) -> Dict:
        """
        Calculate confidence interval for data
        
        Args:
            data: Input data
            confidence: Confidence level (0-1)
            
        Returns:
            Dictionary with interval bounds
        """
        mean = np.mean(data)
        std = np.std(data)
        n = len(data)
        
        # Calculate z-score for confidence level
        from scipy import stats
        z_score = stats.norm.ppf(1 - (1 - confidence) / 2)
        
        margin = z_score * (std / np.sqrt(n))
        
        return {
            'mean': mean,
            'lower': mean - margin,
            'upper': mean + margin,
            'confidence': confidence
        }