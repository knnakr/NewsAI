"""
Test logging middleware functionality.
"""
import logging
from fastapi.testclient import TestClient
from app.main import app


def test_logging_middleware_logs_request_method(caplog):
    """Middleware should log HTTP method."""
    client = TestClient(app)
    with caplog.at_level(logging.INFO):
        response = client.get("/health")
    assert response.status_code == 200
    assert "GET" in caplog.text


def test_logging_middleware_logs_request_path(caplog):
    """Middleware should log request path."""
    client = TestClient(app)
    with caplog.at_level(logging.INFO):
        response = client.get("/health")
    assert response.status_code == 200
    assert "/health" in caplog.text


def test_logging_middleware_logs_status_code(caplog):
    """Middleware should log response status code."""
    client = TestClient(app)
    with caplog.at_level(logging.INFO):
        response = client.get("/health")
    assert response.status_code == 200
    assert "200" in caplog.text


def test_logging_middleware_logs_duration(caplog):
    """Middleware should log request duration in milliseconds."""
    client = TestClient(app)
    with caplog.at_level(logging.INFO):
        response = client.get("/health")
    assert response.status_code == 200
    assert "ms" in caplog.text


def test_logging_middleware_does_not_affect_response():
    """Middleware should not modify response content."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data


def test_logging_middleware_works_with_different_endpoints(caplog):
    """Middleware should work with various endpoints."""
    client = TestClient(app)
    
    # Test /health endpoint
    with caplog.at_level(logging.INFO):
        response = client.get("/health")
    assert response.status_code == 200
    assert "GET /health → 200" in caplog.text
    
    # Test non-existent endpoint (should be 404)
    caplog.clear()
    with caplog.at_level(logging.INFO):
        response = client.get("/nonexistent")
    assert response.status_code == 404
    assert "GET /nonexistent → 404" in caplog.text
