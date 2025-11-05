"""
Main Routes - Page Rendering
"""

from flask import render_template, request, session
from . import main_bp
from datetime import datetime


@main_bp.route('/')
def index():
    """Main configuration page"""
    return render_template('index.html', current_time=datetime.now())


@main_bp.route('/results/<session_id>')
def results(session_id):
    """Results page showing generated data and visualizations"""
    return render_template('results.html', session_id=session_id)


@main_bp.route('/about')
def about():
    """About page with documentation"""
    return render_template('about.html')
