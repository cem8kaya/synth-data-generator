"""
Domain Templates - Predefined configurations for different industries
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List

# UPDATED IMPORTS - use relative imports
from .domain_schema import (
    GeneratorConfig, EntityConfig, MetricConfig, DistributionConfig,
    TimeWindowConfig, SeasonalityConfig, ARIMAConfig, CorrelationConfig,
    DependencyConfig, ValidationConfig, OutputConfig, DomainType
)

class DomainTemplates:
    """Predefined templates for various domains"""
    
    @staticmethod
    def get_template(domain_type: str) -> GeneratorConfig:
        """Get template configuration for a domain"""
        templates = {
            DomainType.TELECOM: DomainTemplates.telecom_template(),
            DomainType.FINANCE: DomainTemplates.finance_template(),
            DomainType.HEALTHCARE: DomainTemplates.healthcare_template(),
            DomainType.MANUFACTURING: DomainTemplates.manufacturing_template(),
            DomainType.ECOMMERCE: DomainTemplates.ecommerce_template(),
            DomainType.IOT: DomainTemplates.iot_template(),
        }
        return templates.get(domain_type, DomainTemplates.custom_template())
    
    @staticmethod
    def telecom_template() -> GeneratorConfig:
        """Telecom/Network domain template"""
        entities = [
            EntityConfig(
                entity_id="CORE_NET_01",
                entity_type="CoreNetwork",
                capacity=100000,
                metrics=[
                    MetricConfig(
                        name="call_setup_rate",
                        display_name="Call Setup Rate",
                        distribution=DistributionConfig(type="poisson", mean=100, std=10),
                        unit="calls/min",
                        category="performance"
                    ),
                    MetricConfig(
                        name="call_success_rate",
                        display_name="Call Success Rate",
                        distribution=DistributionConfig(type="beta", mean=99.5, std=0.3, min_value=95, max_value=100),
                        unit="%",
                        category="quality"
                    ),
                    MetricConfig(
                        name="latency",
                        display_name="Network Latency",
                        distribution=DistributionConfig(type="gamma", mean=50, std=15, min_value=10, max_value=200),
                        unit="ms",
                        category="performance"
                    ),
                ],
                metadata={"location": "datacenter", "tier": "core"}
            )
        ]
        
        return GeneratorConfig(
            seed=42,
            domain_type=DomainType.TELECOM,
            entities=entities,
            time_window=TimeWindowConfig(
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(days=1),
                granularity_minutes=5
            ),
            seasonality=SeasonalityConfig(period_hours=24, amplitude=0.3, harmonics=2),
            arima=ARIMAConfig(ar_order=2, ma_order=1, ar_coef=[0.6, 0.3], ma_coef=[0.4]),
            correlations=[
                CorrelationConfig(source="latency", target="call_success_rate", coefficient=-0.6)
            ],
            validation=ValidationConfig(quality_threshold=0.9),
            output=OutputConfig(output_dir="./output/telecom", format="parquet")
        )
    
    @staticmethod
    def finance_template() -> GeneratorConfig:
        """Finance/Trading domain template"""
        entities = [
            EntityConfig(
                entity_id="TRADING_SYS_01",
                entity_type="TradingSystem",
                capacity=50000,
                metrics=[
                    MetricConfig(
                        name="transaction_volume",
                        display_name="Transaction Volume",
                        distribution=DistributionConfig(type="lognormal", mean=10000, std=3000, min_value=0),
                        unit="transactions/min",
                        category="volume"
                    ),
                    MetricConfig(
                        name="execution_latency",
                        display_name="Execution Latency",
                        distribution=DistributionConfig(type="gamma", mean=10, std=3, min_value=1, max_value=100),
                        unit="ms",
                        category="performance"
                    ),
                    MetricConfig(
                        name="success_rate",
                        display_name="Transaction Success Rate",
                        distribution=DistributionConfig(type="beta", mean=99.9, std=0.1, min_value=99, max_value=100),
                        unit="%",
                        category="quality"
                    ),
                    MetricConfig(
                        name="order_book_depth",
                        display_name="Order Book Depth",
                        distribution=DistributionConfig(type="normal", mean=500, std=100, min_value=0),
                        unit="orders",
                        category="market"
                    ),
                ],
                metadata={"exchange": "NYSE", "asset_class": "equity"}
            )
        ]
        
        return GeneratorConfig(
            seed=42,
            domain_type=DomainType.FINANCE,
            entities=entities,
            time_window=TimeWindowConfig(
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(days=1),
                granularity_minutes=1
            ),
            seasonality=SeasonalityConfig(period_hours=24, amplitude=0.4, harmonics=3),
            correlations=[
                CorrelationConfig(source="transaction_volume", target="execution_latency", coefficient=0.5)
            ],
            validation=ValidationConfig(quality_threshold=0.95),
            output=OutputConfig(output_dir="./output/finance", format="parquet")
        )
    
    @staticmethod
    def healthcare_template() -> GeneratorConfig:
        """Healthcare/Medical domain template"""
        entities = [
            EntityConfig(
                entity_id="ICU_UNIT_01",
                entity_type="ICU",
                capacity=20,
                metrics=[
                    MetricConfig(
                        name="patient_admissions",
                        display_name="Patient Admissions",
                        distribution=DistributionConfig(type="poisson", mean=3, std=1.5),
                        unit="patients/hour",
                        category="operations"
                    ),
                    MetricConfig(
                        name="bed_occupancy_rate",
                        display_name="Bed Occupancy Rate",
                        distribution=DistributionConfig(type="beta", mean=75, std=10, min_value=0, max_value=100),
                        unit="%",
                        category="capacity"
                    ),
                    MetricConfig(
                        name="response_time",
                        display_name="Emergency Response Time",
                        distribution=DistributionConfig(type="gamma", mean=5, std=2, min_value=1, max_value=30),
                        unit="minutes",
                        category="performance"
                    ),
                    MetricConfig(
                        name="equipment_utilization",
                        display_name="Equipment Utilization",
                        distribution=DistributionConfig(type="beta", mean=60, std=15, min_value=0, max_value=100),
                        unit="%",
                        category="resources"
                    ),
                ],
                metadata={"hospital": "General Hospital", "department": "ICU"}
            )
        ]
        
        return GeneratorConfig(
            seed=42,
            domain_type=DomainType.HEALTHCARE,
            entities=entities,
            time_window=TimeWindowConfig(
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(days=7),
                granularity_minutes=30
            ),
            seasonality=SeasonalityConfig(period_hours=24, amplitude=0.2, harmonics=1),
            validation=ValidationConfig(quality_threshold=0.9),
            output=OutputConfig(output_dir="./output/healthcare", format="csv")
        )
    
    @staticmethod
    def manufacturing_template() -> GeneratorConfig:
        """Manufacturing/Production domain template"""
        entities = [
            EntityConfig(
                entity_id="PROD_LINE_01",
                entity_type="ProductionLine",
                capacity=1000,
                metrics=[
                    MetricConfig(
                        name="throughput",
                        display_name="Production Throughput",
                        distribution=DistributionConfig(type="normal", mean=100, std=10, min_value=0),
                        unit="units/hour",
                        category="production"
                    ),
                    MetricConfig(
                        name="defect_rate",
                        display_name="Defect Rate",
                        distribution=DistributionConfig(type="beta", mean=2, std=0.5, min_value=0, max_value=10),
                        unit="%",
                        category="quality"
                    ),
                    MetricConfig(
                        name="machine_utilization",
                        display_name="Machine Utilization",
                        distribution=DistributionConfig(type="beta", mean=85, std=5, min_value=0, max_value=100),
                        unit="%",
                        category="efficiency"
                    ),
                    MetricConfig(
                        name="cycle_time",
                        display_name="Production Cycle Time",
                        distribution=DistributionConfig(type="gamma", mean=45, std=10, min_value=20, max_value=120),
                        unit="seconds",
                        category="performance"
                    ),
                ],
                metadata={"plant": "Factory A", "shift": "day"}
            )
        ]
        
        return GeneratorConfig(
            seed=42,
            domain_type=DomainType.MANUFACTURING,
            entities=entities,
            time_window=TimeWindowConfig(
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(days=1),
                granularity_minutes=10
            ),
            seasonality=SeasonalityConfig(period_hours=8, amplitude=0.15, harmonics=1),
            correlations=[
                CorrelationConfig(source="machine_utilization", target="throughput", coefficient=0.7)
            ],
            validation=ValidationConfig(quality_threshold=0.9),
            output=OutputConfig(output_dir="./output/manufacturing", format="parquet")
        )
    
    @staticmethod
    def ecommerce_template() -> GeneratorConfig:
        """E-commerce/Retail domain template"""
        entities = [
            EntityConfig(
                entity_id="WEBSTORE_01",
                entity_type="OnlineStore",
                capacity=100000,
                metrics=[
                    MetricConfig(
                        name="page_views",
                        display_name="Page Views",
                        distribution=DistributionConfig(type="poisson", mean=500, std=50),
                        unit="views/min",
                        category="traffic"
                    ),
                    MetricConfig(
                        name="conversion_rate",
                        display_name="Conversion Rate",
                        distribution=DistributionConfig(type="beta", mean=3.5, std=0.8, min_value=0, max_value=10),
                        unit="%",
                        category="sales"
                    ),
                    MetricConfig(
                        name="cart_abandonment_rate",
                        display_name="Cart Abandonment Rate",
                        distribution=DistributionConfig(type="beta", mean=70, std=5, min_value=50, max_value=90),
                        unit="%",
                        category="behavior"
                    ),
                    MetricConfig(
                        name="avg_order_value",
                        display_name="Average Order Value",
                        distribution=DistributionConfig(type="lognormal", mean=75, std=30, min_value=10),
                        unit="USD",
                        category="revenue"
                    ),
                ],
                metadata={"platform": "web", "region": "US"}
            )
        ]
        
        return GeneratorConfig(
            seed=42,
            domain_type=DomainType.ECOMMERCE,
            entities=entities,
            time_window=TimeWindowConfig(
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(days=1),
                granularity_minutes=15
            ),
            seasonality=SeasonalityConfig(period_hours=24, amplitude=0.4, harmonics=2),
            correlations=[
                CorrelationConfig(source="page_views", target="conversion_rate", coefficient=0.3)
            ],
            validation=ValidationConfig(quality_threshold=0.9),
            output=OutputConfig(output_dir="./output/ecommerce", format="csv")
        )
    
    @staticmethod
    def iot_template() -> GeneratorConfig:
        """IoT/Sensor domain template"""
        entities = [
            EntityConfig(
                entity_id="SENSOR_CLUSTER_01",
                entity_type="SensorCluster",
                capacity=10000,
                metrics=[
                    MetricConfig(
                        name="temperature",
                        display_name="Temperature",
                        distribution=DistributionConfig(type="normal", mean=22, std=3, min_value=-10, max_value=50),
                        unit="°C",
                        category="environmental"
                    ),
                    MetricConfig(
                        name="humidity",
                        display_name="Humidity",
                        distribution=DistributionConfig(type="beta", mean=60, std=10, min_value=0, max_value=100),
                        unit="%",
                        category="environmental"
                    ),
                    MetricConfig(
                        name="data_rate",
                        display_name="Data Transmission Rate",
                        distribution=DistributionConfig(type="poisson", mean=50, std=10),
                        unit="packets/sec",
                        category="network"
                    ),
                    MetricConfig(
                        name="battery_level",
                        display_name="Battery Level",
                        distribution=DistributionConfig(type="beta", mean=75, std=15, min_value=0, max_value=100),
                        unit="%",
                        category="power"
                    ),
                ],
                metadata={"deployment": "smart_city", "location": "downtown"}
            )
        ]
        
        return GeneratorConfig(
            seed=42,
            domain_type=DomainType.IOT,
            entities=entities,
            time_window=TimeWindowConfig(
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(days=1),
                granularity_minutes=5
            ),
            seasonality=SeasonalityConfig(period_hours=24, amplitude=0.25, harmonics=2),
            correlations=[
                CorrelationConfig(source="temperature", target="humidity", coefficient=-0.4)
            ],
            validation=ValidationConfig(quality_threshold=0.85),
            output=OutputConfig(output_dir="./output/iot", format="parquet")
        )
    
    @staticmethod
    def custom_template() -> GeneratorConfig:
        """Empty template for custom domains"""
        return GeneratorConfig(
            seed=42,
            domain_type=DomainType.CUSTOM,
            entities=[],
            time_window=TimeWindowConfig(
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(days=1),
                granularity_minutes=15
            ),
            validation=ValidationConfig(quality_threshold=0.9),
            output=OutputConfig(output_dir="./output/custom", format="csv")
        )
    
    @staticmethod
    def list_available_templates() -> List[str]:
        """List all available domain templates"""
        return [dt.value for dt in DomainType]
    
    @staticmethod
    def get_template_description(domain_type: str) -> Dict[str, Any]:
        """Get description of a template"""
        descriptions = {
            DomainType.TELECOM: {
                "name": "Telecommunications",
                "description": "Network performance metrics, call data, latency, success rates",
                "typical_metrics": ["call_setup_rate", "call_success_rate", "latency", "throughput"],
                "use_cases": ["Network monitoring", "Capacity planning", "QoS analysis"]
            },
            DomainType.FINANCE: {
                "name": "Financial Services",
                "description": "Trading systems, transaction data, order flow, market metrics",
                "typical_metrics": ["transaction_volume", "execution_latency", "success_rate", "order_book_depth"],
                "use_cases": ["Trading analytics", "Risk management", "Performance monitoring"]
            },
            DomainType.HEALTHCARE: {
                "name": "Healthcare",
                "description": "Patient data, bed occupancy, response times, equipment usage",
                "typical_metrics": ["patient_admissions", "bed_occupancy_rate", "response_time", "equipment_utilization"],
                "use_cases": ["Resource optimization", "Patient flow analysis", "Capacity planning"]
            },
            DomainType.MANUFACTURING: {
                "name": "Manufacturing",
                "description": "Production metrics, quality data, machine utilization, cycle times",
                "typical_metrics": ["throughput", "defect_rate", "machine_utilization", "cycle_time"],
                "use_cases": ["Production optimization", "Quality control", "Predictive maintenance"]
            },
            DomainType.ECOMMERCE: {
                "name": "E-commerce",
                "description": "Website traffic, conversion rates, cart data, revenue metrics",
                "typical_metrics": ["page_views", "conversion_rate", "cart_abandonment_rate", "avg_order_value"],
                "use_cases": ["Marketing analytics", "Customer behavior", "Revenue optimization"]
            },
            DomainType.IOT: {
                "name": "Internet of Things",
                "description": "Sensor data, environmental metrics, network stats, device health",
                "typical_metrics": ["temperature", "humidity", "data_rate", "battery_level"],
                "use_cases": ["Smart cities", "Environmental monitoring", "Asset tracking"]
            },
            DomainType.CUSTOM: {
                "name": "Custom Domain",
                "description": "Build your own domain-specific configuration",
                "typical_metrics": [],
                "use_cases": ["Any custom use case"]
            }
        }
        return descriptions.get(domain_type, descriptions[DomainType.CUSTOM])