"""
Routes package initialization
"""

from flask import Blueprint
from ..generator import generic_api

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import routes after blueprint creation to avoid circular imports
from . import main

__all__ = ['main_bp', 'api_bp']