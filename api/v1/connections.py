"""
Connection Management API Endpoints
Handles CRUD operations for Guacamole connections
"""

from flask import Blueprint, request, jsonify
from typing import Dict, List, Any

connections_bp = Blueprint('connections', __name__)

# Mock data store (in production, this would be a database)
connections_store = {}
connection_id_counter = 1


@connections_bp.route('/connections', methods=['GET'])
def list_connections() -> Dict[str, Any]:
    """List all connections"""
    return jsonify({
        'status': 'success',
        'data': list(connections_store.values()),
        'count': len(connections_store)
    })


@connections_bp.route('/connections', methods=['POST'])
def create_connection() -> Dict[str, Any]:
    """Create a new connection"""
    global connection_id_counter
    
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    required_fields = ['name', 'protocol', 'hostname']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'status': 'error', 
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 400
    
    connection = {
        'id': connection_id_counter,
        'name': data['name'],
        'protocol': data['protocol'],
        'hostname': data['hostname'],
        'port': data.get('port', 22 if data['protocol'] == 'ssh' else 3389),
        'username': data.get('username', ''),
        'created_at': '2025-01-01T00:00:00Z'  # In production, use actual timestamp
    }
    
    connections_store[connection_id_counter] = connection
    connection_id_counter += 1
    
    return jsonify({
        'status': 'success',
        'message': 'Connection created successfully',
        'data': connection
    }), 201


@connections_bp.route('/connections/<int:connection_id>', methods=['GET'])
def get_connection(connection_id: int) -> Dict[str, Any]:
    """Get a specific connection by ID"""
    connection = connections_store.get(connection_id)
    
    if not connection:
        return jsonify({
            'status': 'error',
            'message': 'Connection not found'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': connection
    })


@connections_bp.route('/connections/<int:connection_id>', methods=['PUT'])
def update_connection(connection_id: int) -> Dict[str, Any]:
    """Update an existing connection"""
    connection = connections_store.get(connection_id)
    
    if not connection:
        return jsonify({
            'status': 'error',
            'message': 'Connection not found'
        }), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    # Update connection fields
    updatable_fields = ['name', 'hostname', 'port', 'username']
    for field in updatable_fields:
        if field in data:
            connection[field] = data[field]
    
    connections_store[connection_id] = connection
    
    return jsonify({
        'status': 'success',
        'message': 'Connection updated successfully',
        'data': connection
    })


@connections_bp.route('/connections/<int:connection_id>', methods=['DELETE'])
def delete_connection(connection_id: int) -> Dict[str, Any]:
    """Delete a connection"""
    connection = connections_store.get(connection_id)
    
    if not connection:
        return jsonify({
            'status': 'error',
            'message': 'Connection not found'
        }), 404
    
    del connections_store[connection_id]
    
    return jsonify({
        'status': 'success',
        'message': 'Connection deleted successfully'
    })