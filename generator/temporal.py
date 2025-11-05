"""
Time Series Features: Seasonality and ARIMA patterns
"""

from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


@dataclass
class SeasonalityComponent:
    """Single seasonality component configuration"""
    period_hours: float
    amplitude: float
    phase: float = 0.0


class SeasonalityGenerator:
    """Generate seasonal patterns using Fourier series"""
    
    def __init__(self, components: List[SeasonalityComponent]):
        self.components = components
    
    def generate(self, timestamps: pd.DatetimeIndex) -> np.ndarray:
        """Generate seasonality pattern for given timestamps"""
        if len(self.components) == 0:
            return np.zeros(len(timestamps))
        
        # Convert timestamps to hours since start
        hours = (timestamps - timestamps[0]).total_seconds() / 3600.0
        
        seasonal_pattern = np.zeros(len(timestamps))
        for comp in self.components:
            # Fourier component
            frequency = 2 * np.pi / comp.period_hours
            seasonal_pattern += comp.amplitude * np.sin(frequency * hours + comp.phase)
        
        return seasonal_pattern


class ARIMAGenerator:
    """Simple ARIMA(p,d,q) pattern generator"""
    
    def __init__(self, ar_params: List[float], ma_params: List[float], 
                 noise_std: float = 0.1, seed: Optional[int] = None):
        self.ar_params = np.array(ar_params) if ar_params else np.array([])
        self.ma_params = np.array(ma_params) if ma_params else np.array([])
        self.noise_std = noise_std
        self.rng = np.random.default_rng(seed)
    
    def generate(self, size: int) -> np.ndarray:
        """Generate ARIMA time series"""
        p = len(self.ar_params)
        q = len(self.ma_params)
        
        # Generate white noise
        noise = self.rng.normal(0, self.noise_std, size + max(p, q))
        
        # Initialize series
        series = np.zeros(size + max(p, q))
        
        # Generate ARMA process
        for t in range(max(p, q), size + max(p, q)):
            # AR component
            if p > 0:
                ar_component = np.sum(self.ar_params * series[t-p:t][::-1])
            else:
                ar_component = 0
            
            # MA component
            if q > 0:
                ma_component = np.sum(self.ma_params * noise[t-q:t][::-1])
            else:
                ma_component = 0
            
            series[t] = ar_component + ma_component + noise[t]
        
        return series[-size:]


class ChangePointInjector:
    """Inject change points (level shifts, trend changes) into time series"""
    
    @staticmethod
    def inject_step_change(data: np.ndarray, change_time_idx: int, 
                          magnitude: float) -> np.ndarray:
        """Inject a step change at specified index"""
        result = data.copy()
        result[change_time_idx:] *= (1 + magnitude)
        return result
    
    @staticmethod
    def inject_ramp_change(data: np.ndarray, start_idx: int, 
                          duration_points: int, magnitude: float) -> np.ndarray:
        """Inject a gradual ramp change"""
        result = data.copy()
        end_idx = min(start_idx + duration_points, len(data))
        
        for i in range(start_idx, end_idx):
            progress = (i - start_idx) / duration_points
            result[i:] *= (1 + magnitude * progress)
        
        return result


class TimeWindowGenerator:
    """Generate time windows with configurable granularity"""
    
    @staticmethod
    def generate_timestamps(start_time: datetime, end_time: datetime, 
                           granularity_minutes: int) -> pd.DatetimeIndex:
        """Generate timestamp range with given granularity"""
        return pd.date_range(
            start=start_time,
            end=end_time,
            freq=f'{granularity_minutes}min'
        )
    
    @staticmethod
    def add_time_features(df: pd.DataFrame, timestamp_col: str = 'timestamp') -> pd.DataFrame:
        """Add time-based features to dataframe"""
        df = df.copy()
        df['hour'] = df[timestamp_col].dt.hour
        df['day_of_week'] = df[timestamp_col].dt.dayofweek
        df['day_of_month'] = df[timestamp_col].dt.day
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_business_hours'] = df['hour'].between(9, 17).astype(int)
        return df
