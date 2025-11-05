"""
Generic Synthetic Data Generator - Main Application
"""

from flask import Flask, render_template
from flask_cors import CORS
from pathlib import Path
import os

from config import config
from generator.generic_api import api_bp


def create_app(config_name='development'):
    """Application factory"""
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from generator.generic_api import api_bp  # UPDATED IMPORT
    app.register_blueprint(api_bp)
    
    # Create necessary directories
    Path(app.config['OUTPUT_FOLDER']).mkdir(parents=True, exist_ok=True)
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    
    # Routes
    @app.route('/')
    def index():
        """Main page"""
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        """About page"""
        return render_template('about.html')
    
    @app.route('/templates')
    def templates_page():
        """Domain templates page"""
        return render_template('templates.html')
    
    @app.route('/results')
    def results():
        """Results page"""
        return render_template('results.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        from flask import jsonify
        return jsonify({
            'success': False,
            'error': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import jsonify
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
    
    return app


if __name__ == '__main__':
    # Get configuration from environment
    config_name = os.getenv('FLASK_ENV', 'development')
    
    app = create_app(config_name)
    
    # Run application
    port = int(os.getenv('PORT', 5000))
    debug = config_name == 'development'
    
    print(f"Starting Generic Synthetic Data Generator on port {port}")
    print(f"Debug mode: {debug}")
    print(f"Access at: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)