"""TDD: health endpoint tests written before implementation."""
import pytest
from fastapi.testclient import TestClient


def test_health_returns_200(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_shape(client: TestClient) -> None:
    response = client.get("/health")
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"
    assert "version" in data["data"]


def test_health_meta_is_null(client: TestClient) -> None:
    response = client.get("/health")
    data = response.json()
    assert data["meta"] is None
