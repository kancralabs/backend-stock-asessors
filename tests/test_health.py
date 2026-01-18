import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_health_check_all_services_connected(client: AsyncClient):
    """
    Test health check when all services are connected
    """
    response = await client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "redis" in data
    assert data["database"] == "connected"
    assert data["redis"] == "connected"


@pytest.mark.asyncio
async def test_health_check_structure(client: AsyncClient):
    """
    Test health check response structure
    """
    response = await client.get("/api/v1/health")
    data = response.json()

    # Check required fields
    required_fields = ["status", "database", "redis"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"

    # Check status values
    assert data["status"] in ["healthy", "unhealthy"]


@pytest.mark.asyncio
async def test_ping_endpoint_response(client: AsyncClient):
    """
    Test ping endpoint returns correct response
    """
    response = await client.get("/api/v1/ping")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert data["message"] == "pong"


@pytest.mark.asyncio
async def test_ping_endpoint_fast_response(client: AsyncClient):
    """
    Test ping endpoint responds quickly
    """
    import time

    start = time.time()
    response = await client.get("/api/v1/ping")
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 1.0  # Should respond in less than 1 second
