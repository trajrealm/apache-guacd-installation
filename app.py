"""
Flask application for Apache Guacamole Management API
Version 1.0
"""

from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.connections import connections_bp
from api.v1.users import users_bp
from api.v1.config import config_bp

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Configuration
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    # Register API v1 blueprints with version prefix
    app.register_blueprint(connections_bp, url_prefix='/api/v1')
    app.register_blueprint(users_bp, url_prefix='/api/v1')
    app.register_blueprint(config_bp, url_prefix='/api/v1')
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'message': 'Apache Guacamole Management API',
            'version': '1.0',
            'api_version': 'v1',
            'endpoints': {
                'connections': '/api/v1/connections',
                'users': '/api/v1/users',
                'config': '/api/v1/config'
            }
        })
    
    # API info endpoint
    @app.route('/api')
    def api_info():
        return jsonify({
            'api_name': 'Apache Guacamole Management API',
            'version': 'v1',
            'description': 'RESTful API for managing Apache Guacamole connections, users, and configuration',
            'available_versions': ['v1'],
            'current_version_url': '/api/v1'
        })
    
    # API v1 info endpoint
    @app.route('/api/v1')
    def api_v1_info():
        return jsonify({
            'version': 'v1',
            'description': 'Apache Guacamole Management API Version 1',
            'endpoints': {
                'connections': {
                    'url': '/api/v1/connections',
                    'methods': ['GET', 'POST'],
                    'description': 'Manage Guacamole connections'
                },
                'users': {
                    'url': '/api/v1/users',
                    'methods': ['GET', 'POST'],
                    'description': 'Manage Guacamole users'
                },
                'config': {
                    'url': '/api/v1/config',
                    'methods': ['GET', 'PUT'],
                    'description': 'Manage Guacamole configuration'
                }
            }
        })
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'api_version': 'v1',
            'timestamp': '2025-01-01T00:00:00Z'
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'message': 'Endpoint not found',
            'available_endpoints': [
                '/api/v1/connections',
                '/api/v1/users',
                '/api/v1/config'
            ]
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)