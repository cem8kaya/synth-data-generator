"""
Generic Synthetic Data Generator API
Domain-agnostic REST API with template support
"""


from flask import Blueprint, request, jsonify, send_file
from pathlib import Path
import pandas as pd
from datetime import datetime
import json
import traceback

# UPDATED IMPORTS - use relative imports
from .domain_schema import GeneratorConfig
from .domain_templates import DomainTemplates
from .generic_core import SyntheticDataGenerator

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/templates', methods=['GET'])
def list_templates():
    """List all available domain templates"""
    try:
        templates = DomainTemplates.list_available_templates()
        descriptions = {
            template: DomainTemplates.get_template_description(template)
            for template in templates
        }
        
        return jsonify({
            'success': True,
            'templates': templates,
            'descriptions': descriptions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@api_bp.route('/template/<domain_type>', methods=['GET'])
def get_template(domain_type):
    """Get configuration template for a specific domain"""
    try:
        template = DomainTemplates.get_template(domain_type)
        
        return jsonify({
            'success': True,
            'domain_type': domain_type,
            'config': template.to_dict(),
            'description': DomainTemplates.get_template_description(domain_type)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@api_bp.route('/generate', methods=['POST'])
def generate_data():
    """Generate synthetic data from configuration"""
    try:
        config_data = request.json
        
        # Parse configuration
        config = GeneratorConfig.from_dict(config_data)
        
        # Generate data
        generator = SyntheticDataGenerator(config)
        df = generator.generate()
        
        # Save to file
        output_dir = Path(config.output.output_dir if config.output else './output')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Determine output format
        output_format = config.output.format if config.output else 'csv'
        
        if output_format == 'parquet':
            filename = f'synthetic_data_{timestamp}.parquet'
            filepath = output_dir / filename
            df.to_parquet(filepath, index=False)
        elif output_format == 'json':
            filename = f'synthetic_data_{timestamp}.json'
            filepath = output_dir / filename
            df.to_json(filepath, orient='records', date_format='iso', indent=2)
        else:  # csv
            filename = f'synthetic_data_{timestamp}.csv'
            filepath = output_dir / filename
            df.to_csv(filepath, index=False)
        
        # Generate metadata
        metadata = {
            'generation_time': datetime.now().isoformat(),
            'num_records': len(df),
            'num_entities': len(config.entities),
            'num_metrics': sum(len(e.metrics) for e in config.entities),
            'time_range': {
                'start': config.time_window.start_time.isoformat(),
                'end': config.time_window.end_time.isoformat(),
                'granularity_minutes': config.time_window.granularity_minutes
            },
            'domain_type': config.domain_type,
            'config_seed': config.seed,
            'file_path': str(filepath),
            'file_size_mb': filepath.stat().st_size / (1024 * 1024),
            'columns': list(df.columns)
        }
        
        # Save metadata if configured
        if config.output and config.output.include_metadata:
            metadata_file = output_dir / f'metadata_{timestamp}.json'
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        # Generate preview
        preview_data = df.head(10).to_dict('records')
        
        # Basic statistics
        stats = {}
        for col in df.columns:
            if col != 'timestamp':
                stats[col] = {
                    'mean': float(df[col].mean()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'median': float(df[col].median())
                }
        
        return jsonify({
            'success': True,
            'metadata': metadata,
            'preview': preview_data,
            'statistics': stats,
            'download_url': f'/api/download/{filename}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@api_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download generated file"""
    try:
        # Look for file in output directories
        possible_dirs = ['./output', './output/telecom', './output/finance', 
                        './output/healthcare', './output/manufacturing',
                        './output/ecommerce', './output/iot', './output/custom']
        
        filepath = None
        for dir_path in possible_dirs:
            potential_path = Path(dir_path) / filename
            if potential_path.exists():
                filepath = potential_path
                break
        
        if filepath is None:
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/validate', methods=['POST'])
def validate_config():
    """Validate configuration without generating data"""
    try:
        config_data = request.json
        
        # Try to parse configuration
        config = GeneratorConfig.from_dict(config_data)
        
        # Perform validation checks
        errors = []
        warnings = []
        
        # Check entities
        if not config.entities:
            errors.append("At least one entity is required")
        
        # Check time window
        if not config.time_window:
            errors.append("Time window configuration is required")
        elif config.time_window.start_time >= config.time_window.end_time:
            errors.append("End time must be after start time")
        
        # Check metrics
        total_metrics = sum(len(e.metrics) for e in config.entities)
        if total_metrics == 0:
            errors.append("At least one metric is required")
        
        # Check correlations
        all_metric_names = []
        for entity in config.entities:
            for metric in entity.metrics:
                all_metric_names.append(f"{entity.entity_id}_{metric.name}")
        
        for corr in config.correlations:
            if corr.source not in all_metric_names:
                warnings.append(f"Correlation source '{corr.source}' not found in metrics")
            if corr.target not in all_metric_names:
                warnings.append(f"Correlation target '{corr.target}' not found in metrics")
            if abs(corr.coefficient) > 1:
                errors.append(f"Correlation coefficient must be between -1 and 1")
        
        # Check anomalies
        for anomaly in config.anomalies:
            if anomaly.epicenter not in all_metric_names:
                warnings.append(f"Anomaly epicenter '{anomaly.epicenter}' not found in metrics")
            if not (0 <= anomaly.severity <= 1):
                warnings.append(f"Anomaly severity should be between 0 and 1")
        
        # Estimate generation time and size
        if config.time_window:
            duration_minutes = (config.time_window.end_time - config.time_window.start_time).total_seconds() / 60
            num_windows = int(duration_minutes / config.time_window.granularity_minutes)
            estimated_rows = num_windows
            estimated_size_mb = (estimated_rows * total_metrics * 8) / (1024 * 1024)  # Rough estimate
            
            estimates = {
                'num_windows': num_windows,
                'estimated_rows': estimated_rows,
                'estimated_size_mb': round(estimated_size_mb, 2),
                'estimated_time_seconds': round(num_windows / 1000, 2)  # Rough estimate
            }
        else:
            estimates = {}
        
        return jsonify({
            'success': len(errors) == 0,
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'estimates': estimates,
            'summary': {
                'num_entities': len(config.entities),
                'num_metrics': total_metrics,
                'num_correlations': len(config.correlations),
                'num_anomalies': len(config.anomalies),
                'has_seasonality': config.seasonality is not None,
                'has_arima': config.arima is not None
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'valid': False,
            'errors': [str(e)],
            'traceback': traceback.format_exc()
        }), 400


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'version': '2.0.0',
        'type': 'generic_synthetic_data_generator'
    })


@api_bp.route('/info', methods=['GET'])
def get_info():
    """Get generator information"""
    return jsonify({
        'success': True,
        'generator': {
            'name': 'Generic Synthetic Data Generator',
            'version': '2.0.0',
            'description': 'Domain-agnostic synthetic data generation system',
            'features': [
                'Multiple probability distributions',
                'Correlation modeling',
                'Temporal patterns (seasonality, ARIMA)',
                'Anomaly injection',
                'Change point simulation',
                'Domain templates',
                'Configurable validation'
            ],
            'supported_domains': DomainTemplates.list_available_templates(),
            'supported_distributions': [
                'normal', 'gamma', 'lognormal', 'beta', 
                'poisson', 'exponential', 'uniform'
            ],
            'supported_anomalies': [
                'spike', 'drop', 'oscillation', 'congestion',
                'degradation', 'outage', 'drift'
            ],
            'output_formats': ['csv', 'parquet', 'json']
        }
    })