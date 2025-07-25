"""
User Management API Endpoints
Handles CRUD operations for Guacamole users
"""

from flask import Blueprint, request, jsonify
from typing import Dict, List, Any

users_bp = Blueprint('users', __name__)

# Mock data store (in production, this would be a database)
users_store = {}
user_id_counter = 1


@users_bp.route('/users', methods=['GET'])
def list_users() -> Dict[str, Any]:
    """List all users"""
    # Remove sensitive information from response
    safe_users = []
    for user in users_store.values():
        safe_user = {k: v for k, v in user.items() if k != 'password'}
        safe_users.append(safe_user)
    
    return jsonify({
        'status': 'success',
        'data': safe_users,
        'count': len(safe_users)
    })


@users_bp.route('/users', methods=['POST'])
def create_user() -> Dict[str, Any]:
    """Create a new user"""
    global user_id_counter
    
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    required_fields = ['username', 'password']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'status': 'error', 
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }), 400
    
    # Check if username already exists
    for user in users_store.values():
        if user['username'] == data['username']:
            return jsonify({
                'status': 'error',
                'message': 'Username already exists'
            }), 409
    
    user = {
        'id': user_id_counter,
        'username': data['username'],
        'password': data['password'],  # In production, this should be hashed
        'email': data.get('email', ''),
        'full_name': data.get('full_name', ''),
        'enabled': data.get('enabled', True),
        'created_at': '2025-01-01T00:00:00Z'  # In production, use actual timestamp
    }
    
    users_store[user_id_counter] = user
    user_id_counter += 1
    
    # Remove password from response
    safe_user = {k: v for k, v in user.items() if k != 'password'}
    
    return jsonify({
        'status': 'success',
        'message': 'User created successfully',
        'data': safe_user
    }), 201


@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int) -> Dict[str, Any]:
    """Get a specific user by ID"""
    user = users_store.get(user_id)
    
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    # Remove password from response
    safe_user = {k: v for k, v in user.items() if k != 'password'}
    
    return jsonify({
        'status': 'success',
        'data': safe_user
    })


@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id: int) -> Dict[str, Any]:
    """Update an existing user"""
    user = users_store.get(user_id)
    
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    # Update user fields
    updatable_fields = ['email', 'full_name', 'enabled', 'password']
    for field in updatable_fields:
        if field in data:
            user[field] = data[field]
    
    users_store[user_id] = user
    
    # Remove password from response
    safe_user = {k: v for k, v in user.items() if k != 'password'}
    
    return jsonify({
        'status': 'success',
        'message': 'User updated successfully',
        'data': safe_user
    })


@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int) -> Dict[str, Any]:
    """Delete a user"""
    user = users_store.get(user_id)
    
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    del users_store[user_id]
    
    return jsonify({
        'status': 'success',
        'message': 'User deleted successfully'
    })


@users_bp.route('/users/<int:user_id>/enable', methods=['POST'])
def enable_user(user_id: int) -> Dict[str, Any]:
    """Enable a user account"""
    user = users_store.get(user_id)
    
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    user['enabled'] = True
    users_store[user_id] = user
    
    return jsonify({
        'status': 'success',
        'message': 'User enabled successfully'
    })


@users_bp.route('/users/<int:user_id>/disable', methods=['POST'])
def disable_user(user_id: int) -> Dict[str, Any]:
    """Disable a user account"""
    user = users_store.get(user_id)
    
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    
    user['enabled'] = False
    users_store[user_id] = user
    
    return jsonify({
        'status': 'success',
        'message': 'User disabled successfully'
    })