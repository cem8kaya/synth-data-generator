"""
Data Validation and Quality Assurance
"""

from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Validation result container"""
    passed: bool
    score: float
    issues: List[str]
    warnings: List[str]
    metrics: Dict[str, Any]


class DataValidator:
    """Comprehensive data validation"""
    
    def __init__(self, quality_threshold: float = 0.90):
        self.quality_threshold = quality_threshold
    
    def validate_dataframe(self, df: pd.DataFrame) -> ValidationResult:
        """Validate generated dataframe"""
        issues = []
        warnings = []
        metrics = {}
        
        # Check for missing values
        missing_pct = df.isnull().sum().sum() / (df.shape[0] * df.shape[1])
        metrics['missing_percentage'] = float(missing_pct)
        if missing_pct > 0.01:
            issues.append(f"High missing value percentage: {missing_pct:.2%}")
        
        # Check for infinite values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        inf_count = np.isinf(df[numeric_cols]).sum().sum()
        metrics['infinite_count'] = int(inf_count)
        if inf_count > 0:
            issues.append(f"Found {inf_count} infinite values")
        
        # Check data ranges
        for col in numeric_cols:
            if col == 'timestamp':
                continue
            
            col_min = df[col].min()
            col_max = df[col].max()
            col_std = df[col].std()
            
            # Check for negative values where they shouldn't be
            if 'rate' in col.lower() or 'success' in col.lower():
                if col_min < 0:
                    issues.append(f"{col}: Contains negative values")
                if col_max > 1.0:
                    warnings.append(f"{col}: Values exceed 1.0 for rate metric")
            
            # Check for zero variance
            if col_std == 0:
                warnings.append(f"{col}: Zero variance detected")
        
        # Check temporal continuity
        if 'timestamp' in df.columns:
            time_diffs = df['timestamp'].diff().dt.total_seconds()
            expected_diff = time_diffs.median()
            irregular_gaps = int((time_diffs > expected_diff * 1.5).sum())
            
            if irregular_gaps > len(df) * 0.01:
                warnings.append(f"Irregular time gaps detected: {irregular_gaps} instances")
        
        # Calculate overall quality score
        score = 1.0
        score -= len(issues) * 0.15
        score -= len(warnings) * 0.05
        score = max(0.0, min(1.0, score))
        
        passed = score >= self.quality_threshold and len(issues) == 0
        
        return ValidationResult(
            passed=passed,
            score=float(score),
            issues=issues,
            warnings=warnings,
            metrics=metrics
        )
    
    def validate_statistical_properties(self, data: np.ndarray, 
                                       expected_mean: float,
                                       expected_std: float,
                                       tolerance: float = 0.1) -> Dict[str, Any]:
        """Validate statistical properties of data"""
        actual_mean = np.mean(data)
        actual_std = np.std(data)
        
        mean_error = abs(actual_mean - expected_mean) / expected_mean
        std_error = abs(actual_std - expected_std) / expected_std
        
        return {
            'mean_valid': mean_error < tolerance,
            'std_valid': std_error < tolerance,
            'mean_error': mean_error,
            'std_error': std_error,
            'actual_mean': actual_mean,
            'actual_std': actual_std
        }


class QualityAssessor:
    """Assess overall data quality"""
    
    @staticmethod
    def assess_quality(df: pd.DataFrame) -> Dict[str, Any]:
        """Comprehensive quality assessment"""
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        quality_metrics = {
            'total_rows': int(len(df)),
            'total_columns': int(len(df.columns)),
            'numeric_columns': int(len(numeric_cols)),
            'completeness': float(1.0 - (df.isnull().sum().sum() / (df.shape[0] * df.shape[1]))),
            'duplicates': int(df.duplicated().sum()),
        }
        
        # Statistical properties
        if len(numeric_cols) > 0:
            cv_values = [
                df[col].std() / df[col].mean() if df[col].mean() != 0 else 0
                for col in numeric_cols if col != 'timestamp'
            ]
            quality_metrics['mean_cv'] = float(np.mean(cv_values)) if cv_values else 0.0
        
        # Temporal properties
        if 'timestamp' in df.columns:
            time_diffs = df['timestamp'].diff().dt.total_seconds()
            quality_metrics['time_regularity'] = float(1.0 - (time_diffs.std() / time_diffs.mean()))
        
        # Overall quality score
        quality_score = (
            quality_metrics['completeness'] * 0.4 +
            (1.0 - min(quality_metrics['duplicates'] / len(df), 1.0)) * 0.3 +
            quality_metrics.get('time_regularity', 1.0) * 0.3
        )
        quality_metrics['overall_quality'] = float(quality_score)
        
        return quality_metrics