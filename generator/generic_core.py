"""
Generic Synthetic Data Generator - Core Module
Domain-agnostic implementation with configurable patterns
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from scipy import stats
from scipy.linalg import cholesky

# UPDATED IMPORTS - use relative imports
from .domain_schema import (
    GeneratorConfig, EntityConfig, MetricConfig, DistributionConfig,
    DistributionType, AnomalyType, ChangeType
)


class DistributionGenerator:
    """Generic distribution generator"""
    
    def __init__(self, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed)
    
    def generate(self, config: DistributionConfig, size: int, 
                 adjustment_factor: float = 1.0) -> np.ndarray:
        """Generate values from configured distribution"""
        
        dist_type = config.type.lower()
        mean = config.mean * adjustment_factor
        
        if dist_type == DistributionType.NORMAL:
            std = config.std or mean * 0.1
            values = self.rng.normal(mean, std, size)
        
        elif dist_type == DistributionType.POISSON:
            values = self.rng.poisson(mean, size).astype(float)
        
        elif dist_type == DistributionType.GAMMA:
            # Use CV (coefficient of variation) if provided
            cv = config.params.get('cv', 0.3) if config.params else 0.3
            shape = 1 / (cv ** 2)
            scale = mean / shape
            values = self.rng.gamma(shape, scale, size)
        
        elif dist_type == DistributionType.LOGNORMAL:
            std = config.std or mean * 0.3
            mu = np.log(mean ** 2 / np.sqrt(mean ** 2 + std ** 2))
            sigma = np.sqrt(np.log(1 + (std ** 2 / mean ** 2)))
            values = self.rng.lognormal(mu, sigma, size)
        
        elif dist_type == DistributionType.BETA:
            # Map percentage to 0-1 range
            if config.max_value and config.max_value > 1:
                target_mean = mean / 100.0
                target_std = (config.std or 1.0) / 100.0
            else:
                target_mean = mean
                target_std = config.std or 0.1
            
            # Calculate alpha and beta parameters
            if target_std > 0:
                v = target_std ** 2
                alpha = target_mean * ((target_mean * (1 - target_mean) / v) - 1)
                beta = (1 - target_mean) * ((target_mean * (1 - target_mean) / v) - 1)
                alpha = max(alpha, 0.1)
                beta = max(beta, 0.1)
            else:
                alpha, beta = 10, 10
            
            values = self.rng.beta(alpha, beta, size)
            
            # Scale back to original range
            if config.max_value and config.max_value > 1:
                values = values * 100
        
        elif dist_type == DistributionType.EXPONENTIAL:
            rate = config.params.get('rate', 1.0 / mean) if config.params else 1.0 / mean
            values = self.rng.exponential(1 / rate, size)
        
        elif dist_type == DistributionType.UNIFORM:
            min_val = config.min_value if config.min_value is not None else mean * 0.5
            max_val = config.max_value if config.max_value is not None else mean * 1.5
            values = self.rng.uniform(min_val, max_val, size)
        
        else:
            # Default to normal if unknown
            std = config.std or mean * 0.1
            values = self.rng.normal(mean, std, size)
        
        # Apply constraints
        if config.min_value is not None:
            values = np.maximum(values, config.min_value)
        if config.max_value is not None:
            values = np.minimum(values, config.max_value)
        
        return values


class CorrelationEngine:
    """Handle correlations between metrics using Gaussian copula"""
    
    def __init__(self, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed)
    
    def apply_correlations(self, data: Dict[str, np.ndarray], 
                          correlations: List[Any]) -> Dict[str, np.ndarray]:
        """Apply correlation structure to generated data"""
        
        if not correlations:
            return data
        
        # Build correlation matrix
        metrics = list(data.keys())
        n_metrics = len(metrics)
        corr_matrix = np.eye(n_metrics)
        
        metric_to_idx = {m: i for i, m in enumerate(metrics)}
        
        for corr in correlations:
            if corr.source in metric_to_idx and corr.target in metric_to_idx:
                i = metric_to_idx[corr.source]
                j = metric_to_idx[corr.target]
                corr_matrix[i, j] = corr.coefficient
                corr_matrix[j, i] = corr.coefficient
        
        # Make matrix positive definite
        corr_matrix = self._nearest_positive_definite(corr_matrix)
        
        # Apply correlation using Gaussian copula
        size = len(data[metrics[0]])
        
        # Convert data to uniform using empirical CDF
        uniform_data = np.zeros((size, n_metrics))
        for i, metric in enumerate(metrics):
            sorted_indices = np.argsort(data[metric])
            ranks = np.empty_like(sorted_indices)
            ranks[sorted_indices] = np.arange(size)
            uniform_data[:, i] = (ranks + 1) / (size + 1)
        
        # Transform to normal
        normal_data = stats.norm.ppf(uniform_data)
        
        # Apply correlation
        try:
            L = cholesky(corr_matrix, lower=True)
            correlated_normal = normal_data @ L.T
        except:
            # If Cholesky fails, use original data
            correlated_normal = normal_data
        
        # Transform back to uniform
        correlated_uniform = stats.norm.cdf(correlated_normal)
        
        # Map back to original distributions
        result = {}
        for i, metric in enumerate(metrics):
            sorted_values = np.sort(data[metric])
            indices = np.clip(
                (correlated_uniform[:, i] * size).astype(int),
                0, size - 1
            )
            result[metric] = sorted_values[indices]
        
        return result
    
    def _nearest_positive_definite(self, A: np.ndarray) -> np.ndarray:
        """Find nearest positive definite matrix"""
        B = (A + A.T) / 2
        eigval, eigvec = np.linalg.eigh(B)
        eigval[eigval < 0] = 1e-10
        return eigvec @ np.diag(eigval) @ eigvec.T


class SeasonalityEngine:
    """Add seasonal patterns using Fourier series"""
    
    @staticmethod
    def add_seasonality(data: np.ndarray, timestamps: np.ndarray,
                       config: Any) -> np.ndarray:
        """Add seasonal pattern to data"""
        
        if config is None:
            return data
        
        # Convert timestamps to hours since start
        start_time = timestamps[0]
        hours = np.array([(t - start_time).total_seconds() / 3600 
                         for t in timestamps])
        
        # Create seasonal component
        seasonal = np.zeros_like(data)
        period = config.period_hours
        
        for k in range(1, config.harmonics + 1):
            phase = config.phase_shift if hasattr(config, 'phase_shift') else 0
            seasonal += (config.amplitude / k) * np.sin(
                2 * np.pi * k * hours / period + phase
            )
        
        # Apply seasonality multiplicatively
        return data * (1 + seasonal)


class ARIMAEngine:
    """Apply ARIMA smoothing for temporal coherence"""
    
    def __init__(self, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed)
    
    def apply_arima(self, data: np.ndarray, config: Any) -> np.ndarray:
        """Apply ARIMA model to smooth data"""
        
        if config is None:
            return data
        
        result = data.copy()
        
        # AR component
        for i in range(config.ar_order, len(result)):
            ar_contribution = sum(
                coef * result[i - j - 1] 
                for j, coef in enumerate(config.ar_coef)
            )
            result[i] = 0.3 * ar_contribution + 0.7 * result[i]
        
        # MA component (add noise with moving average smoothing)
        if config.ma_order > 0:
            noise = self.rng.normal(0, config.noise_std * np.std(data), len(data))
            ma_noise = np.zeros_like(noise)
            
            for i in range(config.ma_order, len(noise)):
                ma_noise[i] = sum(
                    coef * noise[i - j - 1]
                    for j, coef in enumerate(config.ma_coef)
                )
            
            result += ma_noise
        
        return result


class ChangePointEngine:
    """Apply change points to data"""
    
    @staticmethod
    def apply_change_points(data: Dict[str, np.ndarray], 
                           timestamps: np.ndarray,
                           change_points: List[Any]) -> Dict[str, np.ndarray]:
        """Apply change points to metrics"""
        
        if not change_points:
            return data
        
        result = {k: v.copy() for k, v in data.items()}
        
        for cp in change_points:
            # Find affected time windows
            start_idx = None
            end_idx = None
            
            for i, ts in enumerate(timestamps):
                if start_idx is None and ts >= cp.start_time:
                    start_idx = i
                if ts >= cp.start_time + timedelta(minutes=cp.duration_minutes):
                    end_idx = i
                    break
            
            if start_idx is None:
                continue
            if end_idx is None:
                end_idx = len(timestamps)
            
            # Apply change to affected metrics
            for metric_name in cp.affected_metrics:
                if metric_name not in result:
                    continue
                
                if cp.change_type == ChangeType.STEP:
                    # Instant change
                    result[metric_name][start_idx:] *= (1 + cp.magnitude)
                
                elif cp.change_type == ChangeType.RAMP:
                    # Gradual change
                    duration = end_idx - start_idx
                    if duration > 0:
                        ramp = np.linspace(0, cp.magnitude, duration)
                        result[metric_name][start_idx:end_idx] *= (1 + ramp)
                        if end_idx < len(result[metric_name]):
                            result[metric_name][end_idx:] *= (1 + cp.magnitude)
        
        return result


class AnomalyEngine:
    """Inject anomalies into data"""
    
    def __init__(self, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed)
    
    def inject_anomalies(self, data: Dict[str, np.ndarray],
                        timestamps: np.ndarray,
                        anomalies: List[Any],
                        dependencies: List[Any]) -> Dict[str, np.ndarray]:
        """Inject configured anomalies"""
        
        if not anomalies:
            return data
        
        result = {k: v.copy() for k, v in data.items()}
        
        for anomaly in anomalies:
            # Find affected time windows
            start_idx = None
            end_idx = None
            
            for i, ts in enumerate(timestamps):
                if start_idx is None and ts >= anomaly.start_time:
                    start_idx = i
                if ts >= anomaly.start_time + timedelta(minutes=anomaly.duration_minutes):
                    end_idx = i
                    break
            
            if start_idx is None:
                continue
            if end_idx is None:
                end_idx = len(timestamps)
            
            # Apply anomaly to epicenter
            if anomaly.epicenter in result:
                result = self._apply_anomaly_pattern(
                    result, anomaly.epicenter, start_idx, end_idx,
                    anomaly.anomaly_type, anomaly.severity
                )
            
            # Propagate if configured
            if anomaly.propagate:
                affected = self._get_dependent_metrics(
                    anomaly.epicenter, dependencies
                )
                for metric in affected:
                    if metric in result:
                        # Reduced severity for propagated anomalies
                        propagated_severity = anomaly.severity * 0.5
                        result = self._apply_anomaly_pattern(
                            result, metric, start_idx, end_idx,
                            anomaly.anomaly_type, propagated_severity
                        )
        
        return result
    
    def _apply_anomaly_pattern(self, data: Dict[str, np.ndarray],
                               metric: str, start_idx: int, end_idx: int,
                               anomaly_type: str, severity: float) -> Dict[str, np.ndarray]:
        """Apply specific anomaly pattern"""
        
        duration = end_idx - start_idx
        
        if anomaly_type == AnomalyType.SPIKE:
            # Sharp increase
            spike = 1 + severity * (1 + 0.5 * np.sin(np.linspace(0, np.pi, duration)))
            data[metric][start_idx:end_idx] *= spike
        
        elif anomaly_type == AnomalyType.DROP:
            # Sharp decrease
            drop = 1 - severity * (1 + 0.5 * np.sin(np.linspace(0, np.pi, duration)))
            data[metric][start_idx:end_idx] *= np.maximum(drop, 0.1)
        
        elif anomaly_type == AnomalyType.OSCILLATION:
            # Oscillating pattern
            oscillation = 1 + severity * np.sin(np.linspace(0, 4 * np.pi, duration))
            data[metric][start_idx:end_idx] *= oscillation
        
        elif anomaly_type == AnomalyType.DEGRADATION:
            # Gradual decline
            degradation = 1 - severity * np.linspace(0, 1, duration)
            data[metric][start_idx:end_idx] *= np.maximum(degradation, 0.2)
        
        elif anomaly_type == AnomalyType.OUTAGE:
            # Complete failure
            data[metric][start_idx:end_idx] *= (1 - severity)
        
        elif anomaly_type == AnomalyType.CONGESTION:
            # Increased variance
            noise = self.rng.normal(1, severity * 0.3, duration)
            data[metric][start_idx:end_idx] *= noise
        
        return data
    
    def _get_dependent_metrics(self, metric: str, 
                               dependencies: List[Any]) -> List[str]:
        """Get metrics that depend on given metric"""
        dependents = []
        for dep in dependencies:
            if dep.parent == metric:
                dependents.append(dep.child)
        return dependents


class SyntheticDataGenerator:
    """Main generator orchestrator"""
    
    def __init__(self, config: GeneratorConfig):
        self.config = config
        self.dist_gen = DistributionGenerator(config.seed)
        self.corr_engine = CorrelationEngine(config.seed)
        self.arima_engine = ARIMAEngine(config.seed)
        self.anomaly_engine = AnomalyEngine(config.seed)
    
    def generate(self) -> pd.DataFrame:
        """Generate synthetic dataset"""
        
        # Generate time windows
        timestamps = self._generate_timestamps()
        n_windows = len(timestamps)
        
        # Generate base data for all metrics
        data = {}
        for entity in self.config.entities:
            for metric in entity.metrics:
                metric_key = f"{entity.entity_id}_{metric.name}"
                values = self.dist_gen.generate(
                    metric.distribution, n_windows
                )
                data[metric_key] = values
        
        # Apply correlations
        if self.config.correlations:
            data = self.corr_engine.apply_correlations(
                data, self.config.correlations
            )
        
        # Apply seasonality
        if self.config.seasonality:
            for key in data:
                data[key] = SeasonalityEngine.add_seasonality(
                    data[key], timestamps, self.config.seasonality
                )
        
        # Apply ARIMA smoothing
        if self.config.arima:
            for key in data:
                data[key] = self.arima_engine.apply_arima(
                    data[key], self.config.arima
                )
        
        # Apply change points
        if self.config.change_points:
            data = ChangePointEngine.apply_change_points(
                data, timestamps, self.config.change_points
            )
        
        # Inject anomalies
        if self.config.anomalies:
            data = self.anomaly_engine.inject_anomalies(
                data, timestamps, self.config.anomalies,
                self.config.dependencies
            )
        
        # Create DataFrame
        df = pd.DataFrame(data)
        df.insert(0, 'timestamp', timestamps)
        
        return df
    
    def _generate_timestamps(self) -> List[datetime]:
        """Generate timestamp sequence"""
        timestamps = []
        current = self.config.time_window.start_time
        delta = timedelta(minutes=self.config.time_window.granularity_minutes)
        
        while current <= self.config.time_window.end_time:
            timestamps.append(current)
            current += delta
        
        return timestamps