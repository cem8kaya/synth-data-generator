"""
Anomaly Injection and Modeling
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import numpy as np
import pandas as pd


class AnomalyType(str, Enum):
    """Types of anomalies"""
    DEGRADATION = "degradation"
    SPIKE = "spike"
    OUTAGE = "outage"
    CONGESTION = "congestion"
    OSCILLATION = "oscillation"


@dataclass
class AnomalyConfig:
    """Configuration for a single anomaly"""
    anomaly_type: AnomalyType
    start_time: datetime
    duration_minutes: int
    severity: float  # 0.0 to 1.0
    affected_metrics: List[str]
    
    def get_end_time(self) -> datetime:
        """Calculate anomaly end time"""
        from datetime import timedelta
        return self.start_time + timedelta(minutes=self.duration_minutes)


class AnomalyInjector:
    """Inject various types of anomalies into time series data"""
    
    def __init__(self, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed)
    
    def inject_anomaly(self, data: np.ndarray, timestamps: pd.DatetimeIndex,
                       config: AnomalyConfig) -> np.ndarray:
        """Inject anomaly based on configuration"""
        
        # Find time window for anomaly
        # Convert datetime objects to pandas Timestamp for comparison
        start_ts = pd.Timestamp(config.start_time)
        end_ts = pd.Timestamp(config.get_end_time())
        
        # Ensure timezone compatibility
        if timestamps.tz is not None:
            # If timestamps have timezone, localize the config times
            if start_ts.tz is None:
                start_ts = start_ts.tz_localize('UTC')
            if end_ts.tz is None:
                end_ts = end_ts.tz_localize('UTC')
        else:
            # If timestamps are timezone-naive, remove timezone from config times
            if start_ts.tz is not None:
                start_ts = start_ts.tz_localize(None)
            if end_ts.tz is not None:
                end_ts = end_ts.tz_localize(None)
        
        mask = (timestamps >= start_ts) & (timestamps < end_ts)
        anomaly_indices = np.where(mask)[0]
        
        if len(anomaly_indices) == 0:
            return data
        
        result = data.copy()
        
        # Apply anomaly based on type
        if config.anomaly_type == AnomalyType.DEGRADATION:
            result = self._inject_degradation(result, anomaly_indices, config.severity)
        elif config.anomaly_type == AnomalyType.SPIKE:
            result = self._inject_spike(result, anomaly_indices, config.severity)
        elif config.anomaly_type == AnomalyType.OUTAGE:
            result = self._inject_outage(result, anomaly_indices, config.severity)
        elif config.anomaly_type == AnomalyType.CONGESTION:
            result = self._inject_congestion(result, anomaly_indices, config.severity)
        elif config.anomaly_type == AnomalyType.OSCILLATION:
            result = self._inject_oscillation(result, anomaly_indices, config.severity)
        
        return result
    
    def _inject_degradation(self, data: np.ndarray, indices: np.ndarray, 
                           severity: float) -> np.ndarray:
        """Gradual performance degradation"""
        result = data.copy()
        
        # Gradual ramp-down
        ramp = np.linspace(1.0, 1.0 - severity, len(indices))
        result[indices] *= ramp
        
        return result
    
    def _inject_spike(self, data: np.ndarray, indices: np.ndarray, 
                     severity: float) -> np.ndarray:
        """Sudden spike in values"""
        result = data.copy()
        
        # Create spike profile (sharp rise, gradual fall)
        spike_profile = np.exp(-np.linspace(0, 3, len(indices)))
        result[indices] *= (1.0 + severity * spike_profile)
        
        return result
    
    def _inject_outage(self, data: np.ndarray, indices: np.ndarray, 
                      severity: float) -> np.ndarray:
        """Complete or partial outage"""
        result = data.copy()
        result[indices] *= (1.0 - severity)
        return result
    
    def _inject_congestion(self, data: np.ndarray, indices: np.ndarray, 
                          severity: float) -> np.ndarray:
        """Network congestion pattern"""
        result = data.copy()
        
        # Add variability during congestion
        noise = self.rng.normal(1.0, severity * 0.2, len(indices))
        congestion_factor = 1.0 + severity * 0.5
        result[indices] *= congestion_factor * noise
        
        return result
    
    def _inject_oscillation(self, data: np.ndarray, indices: np.ndarray, 
                           severity: float) -> np.ndarray:
        """Oscillating pattern"""
        result = data.copy()
        
        # Create oscillation
        t = np.linspace(0, 4 * np.pi, len(indices))
        oscillation = severity * np.sin(t)
        result[indices] *= (1.0 + oscillation)
        
        return result
    
    def inject_multiple_anomalies(self, data: np.ndarray, 
                                   timestamps: pd.DatetimeIndex,
                                   anomaly_configs: List[AnomalyConfig]) -> np.ndarray:
        """Inject multiple anomalies sequentially"""
        result = data.copy()
        
        for config in anomaly_configs:
            result = self.inject_anomaly(result, timestamps, config)
        
        return result


class AnomalyDetector:
    """Simple anomaly detection for validation"""
    
    @staticmethod
    def detect_statistical_anomalies(data: np.ndarray, 
                                     threshold_std: float = 3.0) -> np.ndarray:
        """Detect statistical anomalies using z-score method"""
        mean = np.mean(data)
        std = np.std(data)
        z_scores = np.abs((data - mean) / std)
        return z_scores > threshold_std
    
    @staticmethod
    def detect_point_anomalies(data: np.ndarray, 
                              window_size: int = 10) -> np.ndarray:
        """Detect point anomalies using moving window"""
        anomalies = np.zeros(len(data), dtype=bool)
        
        for i in range(window_size, len(data) - window_size):
            window = np.concatenate([
                data[i-window_size:i],
                data[i+1:i+window_size+1]
            ])
            window_mean = np.mean(window)
            window_std = np.std(window)
            
            if abs(data[i] - window_mean) > 3 * window_std:
                anomalies[i] = True
        
        return anomalies