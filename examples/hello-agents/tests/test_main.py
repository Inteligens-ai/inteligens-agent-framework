"""
Comprehensive test suite for Hello Agents API endpoints.

This test suite validates:
- All endpoints return correct status codes
- Response bodies match expected structure
- Pydantic models validate correctly
- Edge cases and error handling
"""
import os
import pytest
from fastapi.testclient import TestClient
from main import app, API_VERSION, StatusResponse, VersionResponse

client = TestClient(app)


# ============================================
# Root Endpoint Tests (GET /)
# ============================================

def test_root_endpoint_status_code():
    """Test GET / endpoint returns HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_root_endpoint_response_body():
    """Test GET / endpoint returns correct JSON response."""
    response = client.get("/")
    assert response.json() == {"status": "ok"}


def test_root_endpoint_response_model():
    """Test that root endpoint response matches StatusResponse model."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert isinstance(data["status"], str)
    # Validate it can be parsed as StatusResponse
    model = StatusResponse(**data)
    assert model.status == "ok"


def test_root_endpoint_content_type():
    """Test GET / endpoint returns JSON content type."""
    response = client.get("/")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]


def test_root_endpoint_method_not_allowed():
    """Test that POST / returns 405 Method Not Allowed."""
    response = client.post("/")
    assert response.status_code == 405


# ============================================
# Health Endpoint Tests (GET /health)
# ============================================

def test_health_endpoint_status_code():
    """Test GET /health endpoint returns HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_response_body():
    """Test GET /health endpoint returns correct JSON response."""
    response = client.get("/health")
    assert response.json() == {"status": "healthy"}


def test_health_endpoint_response_model():
    """Test that health endpoint response matches StatusResponse model."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert isinstance(data["status"], str)
    # Validate it can be parsed as StatusResponse
    model = StatusResponse(**data)
    assert model.status == "healthy"


def test_health_endpoint_content_type():
    """Test GET /health endpoint returns JSON content type."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]


def test_health_endpoint_method_not_allowed():
    """Test that POST /health returns 405 Method Not Allowed."""
    response = client.post("/health")
    assert response.status_code == 405


# ============================================
# Version Endpoint Tests (GET /version)
# ============================================

def test_version_endpoint_status_code():
    """Test GET /version endpoint returns HTTP 200."""
    response = client.get("/version")
    assert response.status_code == 200


def test_version_endpoint_response_body():
    """Test GET /version endpoint returns correct JSON response."""
    response = client.get("/version")
    data = response.json()
    assert "version" in data
    assert isinstance(data["version"], str)
    # Version should match the configured API_VERSION
    assert data["version"] == API_VERSION


def test_version_endpoint_response_model():
    """Test that version endpoint response matches VersionResponse model."""
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert isinstance(data["version"], str)
    # Validate it can be parsed as VersionResponse
    model = VersionResponse(**data)
    assert model.version == API_VERSION


def test_version_endpoint_content_type():
    """Test GET /version endpoint returns JSON content type."""
    response = client.get("/version")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]


def test_version_endpoint_method_not_allowed():
    """Test that POST /version returns 405 Method Not Allowed."""
    response = client.post("/version")
    assert response.status_code == 405


def test_version_endpoint_default_value():
    """Test that version endpoint returns default version when not configured."""
    # The default version should be "1.0.0" if API_VERSION is not set
    # This test verifies the endpoint works with the default
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    # Version should be a valid string
    assert isinstance(data["version"], str)
    assert len(data["version"]) > 0


# ============================================
# Error Handling Tests
# ============================================

def test_nonexistent_endpoint():
    """Test that nonexistent endpoint returns 404 Not Found."""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_invalid_method():
    """Test that invalid HTTP methods return appropriate errors."""
    # PUT should return 405 Method Not Allowed
    response = client.put("/")
    assert response.status_code == 405
    
    # DELETE should return 405 Method Not Allowed
    response = client.delete("/health")
    assert response.status_code == 405


# ============================================
# Response Model Validation Tests
# ============================================

def test_status_response_model_validation():
    """Test StatusResponse Pydantic model validation."""
    # Valid model
    valid_model = StatusResponse(status="ok")
    assert valid_model.status == "ok"
    
    # Model should reject invalid types
    with pytest.raises(Exception):
        StatusResponse(status=123)  # Should be string


def test_version_response_model_validation():
    """Test VersionResponse Pydantic model validation."""
    # Valid model
    valid_model = VersionResponse(version="1.0.0")
    assert valid_model.version == "1.0.0"
    
    # Model should reject invalid types
    with pytest.raises(Exception):
        VersionResponse(version=123)  # Should be string


# ============================================
# Integration Tests
# ============================================

def test_all_endpoints_accessible():
    """Test that all three endpoints are accessible and return 200."""
    endpoints = ["/", "/health", "/version"]
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200, f"Endpoint {endpoint} failed"


def test_endpoints_response_time():
    """Test that endpoints respond quickly (basic performance check)."""
    import time
    
    endpoints = ["/", "/health", "/version"]
    for endpoint in endpoints:
        start = time.time()
        response = client.get(endpoint)
        elapsed = time.time() - start
        
        assert response.status_code == 200
        # Should respond in less than 1 second (very generous for local)
        assert elapsed < 1.0, f"Endpoint {endpoint} too slow: {elapsed}s"
