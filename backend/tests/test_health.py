"""
Tests for health check endpoint.
"""
import pytest


async def test_health_endpoint_returns_200(client):
    """Health endpoint should return 200 status code."""
    response = await client.get("/health")
    assert response.status_code == 200


async def test_health_endpoint_returns_correct_schema(client):
    """Health endpoint response should contain required fields."""
    response = await client.get("/health")
    data = response.json()
    assert "status" in data
    assert "database" in data


async def test_health_endpoint_db_connected(client):
    """Health endpoint should report database as connected."""
    response = await client.get("/health")
    assert response.json()["database"] == "connected"


async def test_health_endpoint_returns_ok_status(client):
    """Health endpoint should return ok status."""
    response = await client.get("/health")
    assert response.json()["status"] == "ok"
