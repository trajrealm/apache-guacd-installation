"""
Configuration Management API Endpoints
Handles Guacamole configuration settings
"""

from flask import Blueprint, request, jsonify
from typing import Dict, List, Any

config_bp = Blueprint('config', __name__)

# Mock configuration store (in production, this would be a database)
config_store = {
    'database': {
        'mysql-hostname': '127.0.0.1',
        'mysql-port': 3306,
        'mysql-database': 'guacamole_db',
        'mysql-username': 'guacamole_user'
    },
    'server': {
        'guacd-hostname': 'localhost',
        'guacd-port': 4822,
        'guacd-ssl': False
    },
    'security': {
        'session-timeout': 3600,
        'max-concurrent-sessions': 10,
        'password-min-length': 8
    }
}


@config_bp.route('/config', methods=['GET'])
def get_all_config() -> Dict[str, Any]:
    """Get all configuration settings"""
    # Remove sensitive information
    safe_config = {}
    for category, settings in config_store.items():
        safe_config[category] = {}
        for key, value in settings.items():
            # Hide password-related settings
            if 'password' in key.lower():
                safe_config[category][key] = '***'
            else:
                safe_config[category][key] = value
    
    return jsonify({
        'status': 'success',
        'data': safe_config
    })


@config_bp.route('/config/<category>', methods=['GET'])
def get_config_category(category: str) -> Dict[str, Any]:
    """Get configuration settings for a specific category"""
    if category not in config_store:
        return jsonify({
            'status': 'error',
            'message': f'Configuration category "{category}" not found'
        }), 404
    
    # Remove sensitive information
    safe_settings = {}
    for key, value in config_store[category].items():
        if 'password' in key.lower():
            safe_settings[key] = '***'
        else:
            safe_settings[key] = value
    
    return jsonify({
        'status': 'success',
        'data': safe_settings
    })


@config_bp.route('/config/<category>/<setting>', methods=['GET'])
def get_config_setting(category: str, setting: str) -> Dict[str, Any]:
    """Get a specific configuration setting"""
    if category not in config_store:
        return jsonify({
            'status': 'error',
            'message': f'Configuration category "{category}" not found'
        }), 404
    
    if setting not in config_store[category]:
        return jsonify({
            'status': 'error',
            'message': f'Configuration setting "{setting}" not found in category "{category}"'
        }), 404
    
    value = config_store[category][setting]
    
    # Hide sensitive information
    if 'password' in setting.lower():
        value = '***'
    
    return jsonify({
        'status': 'success',
        'data': {
            'category': category,
            'setting': setting,
            'value': value
        }
    })


@config_bp.route('/config/<category>', methods=['PUT'])
def update_config_category(category: str) -> Dict[str, Any]:
    """Update multiple settings in a configuration category"""
    if category not in config_store:
        return jsonify({
            'status': 'error',
            'message': f'Configuration category "{category}" not found'
        }), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    # Update settings
    for setting, value in data.items():
        if setting in config_store[category]:
            config_store[category][setting] = value
    
    return jsonify({
        'status': 'success',
        'message': f'Configuration category "{category}" updated successfully'
    })


@config_bp.route('/config/<category>/<setting>', methods=['PUT'])
def update_config_setting(category: str, setting: str) -> Dict[str, Any]:
    """Update a specific configuration setting"""
    if category not in config_store:
        return jsonify({
            'status': 'error',
            'message': f'Configuration category "{category}" not found'
        }), 404
    
    if setting not in config_store[category]:
        return jsonify({
            'status': 'error',
            'message': f'Configuration setting "{setting}" not found in category "{category}"'
        }), 404
    
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({'status': 'error', 'message': 'No value provided'}), 400
    
    config_store[category][setting] = data['value']
    
    return jsonify({
        'status': 'success',
        'message': f'Configuration setting "{category}.{setting}" updated successfully'
    })


@config_bp.route('/config/validate', methods=['POST'])
def validate_config() -> Dict[str, Any]:
    """Validate current configuration"""
    issues = []
    
    # Check database configuration
    db_config = config_store.get('database', {})
    if not db_config.get('mysql-hostname'):
        issues.append('Database hostname is not configured')
    if not db_config.get('mysql-database'):
        issues.append('Database name is not configured')
    if not db_config.get('mysql-username'):
        issues.append('Database username is not configured')
    
    # Check server configuration
    server_config = config_store.get('server', {})
    if not server_config.get('guacd-hostname'):
        issues.append('Guacd hostname is not configured')
    
    # Check security configuration
    security_config = config_store.get('security', {})
    if security_config.get('password-min-length', 0) < 8:
        issues.append('Password minimum length should be at least 8 characters')
    
    is_valid = len(issues) == 0
    
    return jsonify({
        'status': 'success',
        'data': {
            'valid': is_valid,
            'issues': issues,
            'message': 'Configuration is valid' if is_valid else 'Configuration has issues'
        }
    })


@config_bp.route('/config/backup', methods=['GET'])
def backup_config() -> Dict[str, Any]:
    """Create a backup of current configuration"""
    return jsonify({
        'status': 'success',
        'data': {
            'backup_id': 'backup_20250101_000000',
            'timestamp': '2025-01-01T00:00:00Z',
            'configuration': config_store
        }
    })


@config_bp.route('/config/restore', methods=['POST'])
def restore_config() -> Dict[str, Any]:
    """Restore configuration from backup"""
    data = request.get_json()
    if not data or 'configuration' not in data:
        return jsonify({'status': 'error', 'message': 'No configuration data provided'}), 400
    
    global config_store
    config_store = data['configuration']
    
    return jsonify({
        'status': 'success',
        'message': 'Configuration restored successfully'
    })