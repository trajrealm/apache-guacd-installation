# Apache Guacamole Management API Documentation

## Overview

This API provides RESTful endpoints for managing Apache Guacamole connections, users, and configuration. All APIs are versioned and located under the `/api/v1/` path for proper version management.

## API Version

**Current Version:** v1  
**Base URL:** `http://localhost:5000/api/v1/`

## Authentication

Currently, the API does not implement authentication. In a production environment, you should add proper authentication and authorization mechanisms.

## API Endpoints

### General Information

#### Get API Information
```
GET /api
```
Returns general API information and available versions.

#### Get API v1 Information
```
GET /api/v1
```
Returns detailed information about API version 1 endpoints.

#### Health Check
```
GET /health
```
Returns the health status of the API.

---

### Connections Management

Manage Guacamole connections for various protocols (SSH, RDP, VNC, etc.).

#### List All Connections
```
GET /api/v1/connections
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "name": "Production Server",
      "protocol": "ssh",
      "hostname": "192.168.1.100",
      "port": 22,
      "username": "admin",
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "count": 1
}
```

#### Create Connection
```
POST /api/v1/connections
```

**Request Body:**
```json
{
  "name": "Production Server",
  "protocol": "ssh",
  "hostname": "192.168.1.100",
  "port": 22,
  "username": "admin"
}
```

**Required Fields:**
- `name`: Connection display name
- `protocol`: Protocol type (ssh, rdp, vnc, telnet)
- `hostname`: Target server hostname or IP

**Optional Fields:**
- `port`: Connection port (defaults: SSH=22, RDP=3389)
- `username`: Username for connection

#### Get Connection
```
GET /api/v1/connections/{id}
```

#### Update Connection
```
PUT /api/v1/connections/{id}
```

#### Delete Connection
```
DELETE /api/v1/connections/{id}
```

---

### User Management

Manage Guacamole users and their accounts.

#### List All Users
```
GET /api/v1/users
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "full_name": "Administrator",
      "enabled": true,
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "count": 1
}
```

#### Create User
```
POST /api/v1/users
```

**Request Body:**
```json
{
  "username": "newuser",
  "password": "securepassword123",
  "email": "user@example.com",
  "full_name": "New User",
  "enabled": true
}
```

**Required Fields:**
- `username`: Unique username
- `password`: User password

**Optional Fields:**
- `email`: User email address
- `full_name`: User's full name
- `enabled`: Account status (default: true)

#### Get User
```
GET /api/v1/users/{id}
```

#### Update User
```
PUT /api/v1/users/{id}
```

#### Delete User
```
DELETE /api/v1/users/{id}
```

#### Enable User
```
POST /api/v1/users/{id}/enable
```

#### Disable User
```
POST /api/v1/users/{id}/disable
```

---

### Configuration Management

Manage Guacamole server configuration settings.

#### Get All Configuration
```
GET /api/v1/config
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "database": {
      "mysql-hostname": "127.0.0.1",
      "mysql-port": 3306,
      "mysql-database": "guacamole_db",
      "mysql-username": "guacamole_user"
    },
    "server": {
      "guacd-hostname": "localhost",
      "guacd-port": 4822,
      "guacd-ssl": false
    },
    "security": {
      "session-timeout": 3600,
      "max-concurrent-sessions": 10,
      "password-min-length": 8
    }
  }
}
```

#### Get Configuration Category
```
GET /api/v1/config/{category}
```

Available categories:
- `database`: Database connection settings
- `server`: Guacd server settings
- `security`: Security and session settings

#### Get Specific Configuration Setting
```
GET /api/v1/config/{category}/{setting}
```

#### Update Configuration Category
```
PUT /api/v1/config/{category}
```

**Request Body:**
```json
{
  "mysql-hostname": "localhost",
  "mysql-port": 3306
}
```

#### Update Specific Configuration Setting
```
PUT /api/v1/config/{category}/{setting}
```

**Request Body:**
```json
{
  "value": "new_value"
}
```

#### Validate Configuration
```
POST /api/v1/config/validate
```

#### Backup Configuration
```
GET /api/v1/config/backup
```

#### Restore Configuration
```
POST /api/v1/config/restore
```

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "status": "error",
  "message": "Description of the error"
}
```

### HTTP Status Codes

- `200`: Success
- `201`: Created successfully
- `400`: Bad request (missing/invalid data)
- `404`: Resource not found
- `409`: Conflict (e.g., username already exists)
- `500`: Internal server error

---

## Examples

### Create SSH Connection
```bash
curl -X POST http://localhost:5000/api/v1/connections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Web Server",
    "protocol": "ssh",
    "hostname": "192.168.1.50",
    "port": 22,
    "username": "webadmin"
  }'
```

### Create User
```bash
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123",
    "email": "john@example.com",
    "full_name": "John Doe"
  }'
```

### Update Database Configuration
```bash
curl -X PUT http://localhost:5000/api/v1/config/database \
  -H "Content-Type: application/json" \
  -d '{
    "mysql-hostname": "db.example.com",
    "mysql-port": 3306
  }'
```

---

## Version Management

The API is designed with version management in mind:

- **Current Version:** v1 (located in `/api/v1/`)
- **Future Versions:** Can be added as `/api/v2/`, `/api/v3/`, etc.
- **Version Discovery:** Use `GET /api` to discover available versions
- **Backward Compatibility:** Older versions remain available

This structure allows for:
- Easy migration between API versions
- Maintaining backward compatibility
- Clear separation of API evolution
- Client applications can choose their preferred version

---

## Running the API

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   python app.py
   ```

3. The API will be available at `http://localhost:5000`

4. Test the API:
   ```bash
   python test_api.py
   ```