"""TDD: /items endpoint tests."""
from unittest.mock import patch, MagicMock
from uuid import uuid4
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.models.item import ItemResponse, Meta


def _item() -> ItemResponse:
    return ItemResponse(
        id=uuid4(), source_id=uuid4(), source_name="arXiv",
        title="Test", url="https://example.com", category="research",
        created_at=datetime.now(timezone.utc),
    )


def _make_client() -> TestClient:
    with patch("app.db.client.create_client", return_value=MagicMock()):
        from app.main import app
        return TestClient(app)


def test_get_items_returns_200() -> None:
    with patch("app.routers.items.find_all", return_value=([], 0)):
        c = _make_client()
        resp = c.get("/items")
        assert resp.status_code == 200


def test_get_items_response_envelope() -> None:
    with patch("app.routers.items.find_all", return_value=([], 0)):
        c = _make_client()
        data = c.get("/items").json()
        assert "success" in data and "data" in data and "meta" in data


def test_get_items_meta_fields() -> None:
    with patch("app.routers.items.find_all", return_value=([_item()], 1)):
        c = _make_client()
        meta = c.get("/items").json()["meta"]
        assert "total" in meta and "limit" in meta and "offset" in meta


def test_get_items_default_limit() -> None:
    captured = {}
    def mock_find_all(**kwargs):
        captured.update(kwargs)
        return [], 0
    with patch("app.routers.items.find_all", side_effect=mock_find_all):
        _make_client().get("/items")
        assert captured.get("limit") == 10


def test_get_items_limit_over_100_returns_422() -> None:
    captured = {}
    def mock_find_all(**kwargs):
        captured.update(kwargs)
        return [], 0
    with patch("app.routers.items.find_all", side_effect=mock_find_all):
        resp = _make_client().get("/items?limit=999")
        assert resp.status_code == 422


def test_mark_read_returns_204() -> None:
    item_id = str(uuid4())
    mock_client = MagicMock()
    mock_client.table.return_value.upsert.return_value.execute.return_value.data = []
    with patch("app.routers.items.get_client", return_value=mock_client):
        c = _make_client()
        resp = c.post(f"/items/{item_id}/read")
        assert resp.status_code == 204


def test_mark_read_invalid_uuid_returns_422() -> None:
    c = _make_client()
    resp = c.post("/items/not-a-uuid/read")
    assert resp.status_code == 422
