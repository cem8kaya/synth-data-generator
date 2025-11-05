"""
Generic Domain Schema Configuration
Replaces telecom-specific schemas with configurable domain patterns
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
import json


class DistributionType(str, Enum):
    """Supported probability distributions"""
    NORMAL = "normal"
    GAMMA = "gamma"
    LOGNORMAL = "lognormal"
    BETA = "beta"
    POISSON = "poisson"
    EXPONENTIAL = "exponential"
    UNIFORM = "uniform"


class AnomalyType(str, Enum):
    """Generic anomaly patterns"""
    SPIKE = "spike"
    DROP = "drop"
    OSCILLATION = "oscillation"
    CONGESTION = "congestion"
    DEGRADATION = "degradation"
    OUTAGE = "outage"
    DRIFT = "drift"


class ChangeType(str, Enum):
    """Change point patterns"""
    RAMP = "ramp"  # Gradual change
    STEP = "step"  # Instant change
    SEASONAL = "seasonal"  # Recurring pattern change


class DomainType(str, Enum):
    """Predefined domain templates"""
    TELECOM = "telecom"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    MANUFACTURING = "manufacturing"
    ECOMMERCE = "ecommerce"
    IOT = "iot"
    CUSTOM = "custom"


@dataclass
class DistributionConfig:
    """Generic distribution configuration"""
    type: str
    mean: float
    std: Optional[float] = None
    
    # Generic parameters
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    
    # Distribution-specific parameters (optional)
    params: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'type': self.type,
            'mean': self.mean,
        }
        if self.std is not None:
            result['std'] = self.std
        if self.min_value is not None:
            result['min_value'] = self.min_value
        if self.max_value is not None:
            result['max_value'] = self.max_value
        if self.params:
            result['params'] = self.params
        return result


@dataclass
class MetricConfig:
    """Generic metric configuration"""
    name: str
    display_name: str
    distribution: DistributionConfig
    unit: str = ""
    category: str = "general"
    dependencies: List[str] = field(default_factory=list)
    constraints: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'display_name': self.display_name,
            'distribution': self.distribution.to_dict(),
            'unit': self.unit,
            'category': self.category,
            'dependencies': self.dependencies,
            'constraints': self.constraints
        }


@dataclass
class EntityConfig:
    """Generic entity (replaces node/component concept)"""
    entity_id: str
    entity_type: str
    capacity: Optional[float] = None
    metrics: List[MetricConfig] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'entity_id': self.entity_id,
            'entity_type': self.entity_type,
            'capacity': self.capacity,
            'metrics': [m.to_dict() for m in self.metrics],
            'metadata': self.metadata
        }


@dataclass
class CorrelationConfig:
    """Correlation between metrics"""
    source: str
    target: str
    coefficient: float
    lag: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'source': self.source,
            'target': self.target,
            'coefficient': self.coefficient,
            'lag': self.lag
        }


@dataclass
class DependencyConfig:
    """Causal dependency between metrics"""
    parent: str
    child: str
    influence_factor: float
    delay_minutes: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'parent': self.parent,
            'child': self.child,
            'influence_factor': self.influence_factor,
            'delay_minutes': self.delay_minutes
        }


@dataclass
class SeasonalityConfig:
    """Seasonality pattern configuration"""
    period_hours: float
    amplitude: float
    harmonics: int = 1
    phase_shift: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'period_hours': self.period_hours,
            'amplitude': self.amplitude,
            'harmonics': self.harmonics,
            'phase_shift': self.phase_shift
        }


@dataclass
class ARIMAConfig:
    """ARIMA model configuration"""
    ar_order: int = 1
    ma_order: int = 1
    ar_coef: List[float] = field(default_factory=lambda: [0.5])
    ma_coef: List[float] = field(default_factory=lambda: [0.3])
    noise_std: float = 0.05
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'ar_order': self.ar_order,
            'ma_order': self.ma_order,
            'ar_coef': self.ar_coef,
            'ma_coef': self.ma_coef,
            'noise_std': self.noise_std
        }


@dataclass
class ChangePointConfig:
    """Change point configuration"""
    change_id: str
    change_type: str
    affected_metrics: List[str]
    start_time: datetime
    duration_minutes: int
    magnitude: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'change_id': self.change_id,
            'change_type': self.change_type,
            'affected_metrics': self.affected_metrics,
            'start_time': self.start_time.isoformat(),
            'duration_minutes': self.duration_minutes,
            'magnitude': self.magnitude
        }


@dataclass
class AnomalyConfig:
    """Anomaly configuration"""
    anomaly_id: str
    anomaly_type: str
    start_time: datetime
    duration_minutes: int
    severity: float
    epicenter: str
    propagate: bool = False
    affected_entities: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'anomaly_id': self.anomaly_id,
            'anomaly_type': self.anomaly_type,
            'start_time': self.start_time.isoformat(),
            'duration_minutes': self.duration_minutes,
            'severity': self.severity,
            'epicenter': self.epicenter,
            'propagate': self.propagate,
            'affected_entities': self.affected_entities
        }


@dataclass
class TimeWindowConfig:
    """Time window configuration"""
    start_time: datetime
    end_time: datetime
    granularity_minutes: int = 5
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'granularity_minutes': self.granularity_minutes
        }


@dataclass
class ValidationConfig:
    """Validation configuration"""
    quality_threshold: float = 0.9
    statistical_weight: float = 0.25
    logical_weight: float = 0.25
    causal_weight: float = 0.20
    temporal_weight: float = 0.15
    domain_weight: float = 0.15
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'quality_threshold': self.quality_threshold,
            'statistical_weight': self.statistical_weight,
            'logical_weight': self.logical_weight,
            'causal_weight': self.causal_weight,
            'temporal_weight': self.temporal_weight,
            'domain_weight': self.domain_weight
        }


@dataclass
class OutputConfig:
    """Output configuration"""
    output_dir: str = "./output"
    format: str = "parquet"
    compress: bool = True
    include_metadata: bool = True
    chunk_size: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'output_dir': self.output_dir,
            'format': self.format,
            'compress': self.compress,
            'include_metadata': self.include_metadata,
            'chunk_size': self.chunk_size
        }


@dataclass
class GeneratorConfig:
    """Main generator configuration"""
    seed: int
    domain_type: str = "custom"
    entities: List[EntityConfig] = field(default_factory=list)
    time_window: Optional[TimeWindowConfig] = None
    seasonality: Optional[SeasonalityConfig] = None
    arima: Optional[ARIMAConfig] = None
    correlations: List[CorrelationConfig] = field(default_factory=list)
    dependencies: List[DependencyConfig] = field(default_factory=list)
    change_points: List[ChangePointConfig] = field(default_factory=list)
    anomalies: List[AnomalyConfig] = field(default_factory=list)
    validation: Optional[ValidationConfig] = None
    output: Optional[OutputConfig] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'seed': self.seed,
            'domain_type': self.domain_type,
            'entities': [e.to_dict() for e in self.entities],
        }
        if self.time_window:
            result['time_window'] = self.time_window.to_dict()
        if self.seasonality:
            result['seasonality'] = self.seasonality.to_dict()
        if self.arima:
            result['arima'] = self.arima.to_dict()
        if self.correlations:
            result['correlations'] = [c.to_dict() for c in self.correlations]
        if self.dependencies:
            result['dependencies'] = [d.to_dict() for d in self.dependencies]
        if self.change_points:
            result['change_points'] = [cp.to_dict() for cp in self.change_points]
        if self.anomalies:
            result['anomalies'] = [a.to_dict() for a in self.anomalies]
        if self.validation:
            result['validation'] = self.validation.to_dict()
        if self.output:
            result['output'] = self.output.to_dict()
        return result
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GeneratorConfig':
        """Create from dictionary"""
        # Parse entities
        entities = []
        for entity_data in data.get('entities', []):
            metrics = []
            for metric_data in entity_data.get('metrics', []):
                dist_data = metric_data['distribution']
                distribution = DistributionConfig(
                    type=dist_data['type'],
                    mean=dist_data['mean'],
                    std=dist_data.get('std'),
                    min_value=dist_data.get('min_value'),
                    max_value=dist_data.get('max_value'),
                    params=dist_data.get('params', {})
                )
                metric = MetricConfig(
                    name=metric_data['name'],
                    display_name=metric_data.get('display_name', metric_data['name']),
                    distribution=distribution,
                    unit=metric_data.get('unit', ''),
                    category=metric_data.get('category', 'general'),
                    dependencies=metric_data.get('dependencies', []),
                    constraints=metric_data.get('constraints', {})
                )
                metrics.append(metric)
            
            entity = EntityConfig(
                entity_id=entity_data['entity_id'],
                entity_type=entity_data['entity_type'],
                capacity=entity_data.get('capacity'),
                metrics=metrics,
                metadata=entity_data.get('metadata', {})
            )
            entities.append(entity)
        
        # Parse time window
        time_window = None
        if 'time_window' in data:
            tw_data = data['time_window']
            time_window = TimeWindowConfig(
                start_time=datetime.fromisoformat(tw_data['start_time']),
                end_time=datetime.fromisoformat(tw_data['end_time']),
                granularity_minutes=tw_data.get('granularity_minutes', 5)
            )
        
        # Parse other configs (seasonality, arima, etc.)
        seasonality = None
        if 'seasonality' in data and data['seasonality']:
            s_data = data['seasonality']
            seasonality = SeasonalityConfig(**s_data)
        
        arima = None
        if 'arima' in data and data['arima']:
            a_data = data['arima']
            arima = ARIMAConfig(**a_data)
        
        correlations = [CorrelationConfig(**c) for c in data.get('correlations', [])]
        dependencies = [DependencyConfig(**d) for d in data.get('dependencies', [])]
        
        change_points = []
        for cp_data in data.get('change_points', []):
            cp_data['start_time'] = datetime.fromisoformat(cp_data['start_time'])
            change_points.append(ChangePointConfig(**cp_data))
        
        anomalies = []
        for a_data in data.get('anomalies', []):
            a_data['start_time'] = datetime.fromisoformat(a_data['start_time'])
            anomalies.append(AnomalyConfig(**a_data))
        
        validation = None
        if 'validation' in data and data['validation']:
            validation = ValidationConfig(**data['validation'])
        
        output = None
        if 'output' in data and data['output']:
            output = OutputConfig(**data['output'])
        
        return cls(
            seed=data['seed'],
            domain_type=data.get('domain_type', 'custom'),
            entities=entities,
            time_window=time_window,
            seasonality=seasonality,
            arima=arima,
            correlations=correlations,
            dependencies=dependencies,
            change_points=change_points,
            anomalies=anomalies,
            validation=validation,
            output=output
        )