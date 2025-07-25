#!/usr/bin/env python3
"""
Test script for Apache Guacamole Management API
"""

import requests
import json
import sys
import time
from typing import Dict, Any

API_BASE_URL = "http://localhost:5000"

def test_endpoint(method: str, endpoint: str, data: Dict = None) -> Dict[str, Any]:
    """Test an API endpoint"""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return {
            'status_code': response.status_code,
            'success': response.status_code < 400,
            'data': response.json() if response.content else None
        }
    except Exception as e:
        return {
            'status_code': 0,
            'success': False,
            'error': str(e)
        }

def run_tests():
    """Run comprehensive API tests"""
    print("🚀 Starting Apache Guacamole Management API Tests")
    print("=" * 60)
    
    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    result = test_endpoint('GET', '/')
    if result['success']:
        print("✅ Root endpoint working")
        print(f"   API Version: {result['data'].get('version')}")
    else:
        print("❌ Root endpoint failed")
        return False
    
    # Test 2: API info endpoints
    print("\n2. Testing API info endpoints...")
    for endpoint in ['/api', '/api/v1']:
        result = test_endpoint('GET', endpoint)
        if result['success']:
            print(f"✅ {endpoint} working")
        else:
            print(f"❌ {endpoint} failed")
            return False
    
    # Test 3: Health check
    print("\n3. Testing health check...")
    result = test_endpoint('GET', '/health')
    if result['success']:
        print("✅ Health check working")
    else:
        print("❌ Health check failed")
        return False
    
    # Test 4: Connections API
    print("\n4. Testing Connections API...")
    
    # List connections (should be empty initially)
    result = test_endpoint('GET', '/api/v1/connections')
    if result['success']:
        print("✅ List connections working")
        print(f"   Initial count: {result['data'].get('count', 0)}")
    else:
        print("❌ List connections failed")
        return False
    
    # Create a connection
    connection_data = {
        'name': 'Test SSH Connection',
        'protocol': 'ssh',
        'hostname': '192.168.1.100',
        'port': 22,
        'username': 'testuser'
    }
    result = test_endpoint('POST', '/api/v1/connections', connection_data)
    if result['success']:
        print("✅ Create connection working")
        connection_id = result['data']['data']['id']
        print(f"   Created connection ID: {connection_id}")
    else:
        print("❌ Create connection failed")
        return False
    
    # Get the created connection
    result = test_endpoint('GET', f'/api/v1/connections/{connection_id}')
    if result['success']:
        print("✅ Get connection working")
    else:
        print("❌ Get connection failed")
        return False
    
    # Test 5: Users API
    print("\n5. Testing Users API...")
    
    # List users (should be empty initially)
    result = test_endpoint('GET', '/api/v1/users')
    if result['success']:
        print("✅ List users working")
        print(f"   Initial count: {result['data'].get('count', 0)}")
    else:
        print("❌ List users failed")
        return False
    
    # Create a user
    user_data = {
        'username': 'testuser',
        'password': 'testpassword123',
        'email': 'test@example.com',
        'full_name': 'Test User'
    }
    result = test_endpoint('POST', '/api/v1/users', user_data)
    if result['success']:
        print("✅ Create user working")
        user_id = result['data']['data']['id']
        print(f"   Created user ID: {user_id}")
    else:
        print("❌ Create user failed")
        return False
    
    # Test 6: Configuration API
    print("\n6. Testing Configuration API...")
    
    # Get all configuration
    result = test_endpoint('GET', '/api/v1/config')
    if result['success']:
        print("✅ Get all configuration working")
        categories = list(result['data']['data'].keys())
        print(f"   Configuration categories: {categories}")
    else:
        print("❌ Get configuration failed")
        return False
    
    # Get database configuration
    result = test_endpoint('GET', '/api/v1/config/database')
    if result['success']:
        print("✅ Get database configuration working")
    else:
        print("❌ Get database configuration failed")
        return False
    
    # Validate configuration
    result = test_endpoint('POST', '/api/v1/config/validate')
    if result['success']:
        print("✅ Configuration validation working")
        is_valid = result['data']['data']['valid']
        print(f"   Configuration valid: {is_valid}")
    else:
        print("❌ Configuration validation failed")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All API tests passed successfully!")
    print("\nAPI Structure Summary:")
    print("📁 /api/v1/connections - Connection management")
    print("📁 /api/v1/users - User management") 
    print("📁 /api/v1/config - Configuration management")
    print("\n✨ APIs are now properly versioned in the v1 folder!")
    
    return True

if __name__ == '__main__':
    print("⏳ Waiting for server to start...")
    time.sleep(2)  # Give server time to start
    
    success = run_tests()
    sys.exit(0 if success else 1)