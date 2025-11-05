"""
Statistical Distribution Generators
Adapted from telecom_synthetic_generator_notebook.py
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass
import numpy as np
from scipy import stats
from scipy.special import gamma as gamma_func


class DistributionType(str, Enum):
    """Supported probability distributions"""
    POISSON = "poisson"
    GAMMA = "gamma"
    LOGNORMAL = "lognormal"
    BETA = "beta"


@dataclass
class Context:
    """Dynamic parameter adjustment context"""
    congestion_factor: float = 1.0
    load_factor: float = 1.0
    anomaly_active: bool = False
    anomaly_severity: float = 0.0
    time_of_day: int = 12
    day_of_week: int = 1
    
    def get_adjustment_factor(self) -> float:
        """Calculate combined adjustment factor"""
        factor = 1.0
        if self.congestion_factor > 1.0:
            factor *= self.congestion_factor
        if self.load_factor > 1.0:
            factor *= (1.0 + (self.load_factor - 1.0) * 0.5)
        if self.anomaly_active:
            factor *= (1.0 + self.anomaly_severity)
        return factor


class DistributionGenerator(ABC):
    """Abstract base class for all distribution generators"""
    
    def __init__(self, seed: Optional[int] = None):
        self.rng = np.random.default_rng(seed)
        self._validate_parameters()
    
    @abstractmethod
    def _validate_parameters(self) -> None:
        """Validate distribution parameters"""
        pass
    
    @abstractmethod
    def generate(self, size: int, context: Optional[Context] = None) -> np.ndarray:
        """Generate random values from distribution"""
        pass
    
    @abstractmethod
    def get_theoretical_mean(self) -> float:
        """Return theoretical mean of distribution"""
        pass
    
    @abstractmethod
    def get_theoretical_std(self) -> float:
        """Return theoretical standard deviation"""
        pass
    
    def validate_generated(self, values: np.ndarray) -> Dict[str, Any]:
        """Validate generated values against distribution properties"""
        empirical_mean = np.mean(values)
        empirical_std = np.std(values)
        theoretical_mean = self.get_theoretical_mean()
        theoretical_std = self.get_theoretical_std()
        
        mean_error = abs(empirical_mean - theoretical_mean) / theoretical_mean
        std_error = abs(empirical_std - theoretical_std) / theoretical_std
        
        return {
            "empirical_mean": empirical_mean,
            "theoretical_mean": theoretical_mean,
            "mean_relative_error": mean_error,
            "empirical_std": empirical_std,
            "theoretical_std": theoretical_std,
            "std_relative_error": std_error,
            "mean_valid": mean_error < 0.05,
            "std_valid": std_error < 0.10,
        }


class GammaGenerator(DistributionGenerator):
    """Gamma distribution generator for latency/duration metrics"""
    
    def __init__(self, mean: float, cv: float, seed: Optional[int] = None):
        self.mean = mean
        self.cv = cv
        self.shape = 1 / (cv ** 2)
        self.scale = mean * (cv ** 2)
        super().__init__(seed)
    
    def _validate_parameters(self) -> None:
        if self.mean <= 0:
            raise ValueError("Mean must be positive")
        if self.cv <= 0:
            raise ValueError("CV must be positive")
    
    def generate(self, size: int, context: Optional[Context] = None) -> np.ndarray:
        values = self.rng.gamma(self.shape, self.scale, size)
        if context:
            adjustment = context.get_adjustment_factor()
            values *= adjustment
        return values
    
    def get_theoretical_mean(self) -> float:
        return self.mean
    
    def get_theoretical_std(self) -> float:
        return self.mean * self.cv


class LognormalGenerator(DistributionGenerator):
    """Lognormal distribution generator for throughput/bandwidth metrics"""
    
    def __init__(self, median: float, cv: float, seed: Optional[int] = None):
        self.median = median
        self.cv = cv
        self.sigma = np.sqrt(np.log(1 + cv ** 2))
        self.mu = np.log(median)
        super().__init__(seed)
    
    def _validate_parameters(self) -> None:
        if self.median <= 0:
            raise ValueError("Median must be positive")
        if self.cv <= 0:
            raise ValueError("CV must be positive")
    
    def generate(self, size: int, context: Optional[Context] = None) -> np.ndarray:
        values = self.rng.lognormal(self.mu, self.sigma, size)
        if context:
            adjustment = context.get_adjustment_factor()
            values *= adjustment
        return values
    
    def get_theoretical_mean(self) -> float:
        return self.median * np.exp(0.5 * self.sigma ** 2)
    
    def get_theoretical_std(self) -> float:
        mean = self.get_theoretical_mean()
        return mean * self.cv


class BetaGenerator(DistributionGenerator):
    """Beta distribution generator for success rate metrics"""
    
    def __init__(self, mean: float, cv: float, seed: Optional[int] = None):
        self.mean = mean
        self.cv = cv
        
        # Compute alpha and beta from mean and CV
        variance = (mean * cv) ** 2
        if variance >= mean * (1 - mean):
            variance = mean * (1 - mean) * 0.99
        
        common_term = (mean * (1 - mean) / variance) - 1
        self.alpha = mean * common_term
        self.beta = (1 - mean) * common_term
        
        super().__init__(seed)
    
    def _validate_parameters(self) -> None:
        if not (0 < self.mean < 1):
            raise ValueError("Mean must be between 0 and 1")
        if self.cv <= 0:
            raise ValueError("CV must be positive")
    
    def generate(self, size: int, context: Optional[Context] = None) -> np.ndarray:
        values = self.rng.beta(self.alpha, self.beta, size)
        if context and context.anomaly_active:
            degradation = context.anomaly_severity
            values *= (1 - degradation)
        return values
    
    def get_theoretical_mean(self) -> float:
        return self.mean
    
    def get_theoretical_std(self) -> float:
        return self.mean * self.cv


class PoissonGenerator(DistributionGenerator):
    """Poisson distribution generator for count-based metrics"""
    
    def __init__(self, rate: float, seed: Optional[int] = None):
        self.rate = rate
        super().__init__(seed)
    
    def _validate_parameters(self) -> None:
        if self.rate <= 0:
            raise ValueError("Rate must be positive")
    
    def generate(self, size: int, context: Optional[Context] = None) -> np.ndarray:
        effective_rate = self.rate
        if context:
            effective_rate *= context.get_adjustment_factor()
        return self.rng.poisson(effective_rate, size)
    
    def get_theoretical_mean(self) -> float:
        return self.rate
    
    def get_theoretical_std(self) -> float:
        return np.sqrt(self.rate)
