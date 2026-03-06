"""TDD: /sources endpoint tests."""
from unittest.mock import patch, MagicMock
from uuid import uuid4
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from app.models.source import Source, SourceResponse


def _source(source_id: str | None = None) -> Source:
    return Source(
        id=source_id or str(uuid4()),
        name="arXiv cs.AI",
        url="https://export.arxiv.org/rss/cs.AI",
        type="rss",
        category="research",
        priority="high",
        status="active",
        fetch_config={"adapter": "arxiv"},
        consecutive_failures=0,
        created_at=datetime.now(timezone.utc),
    )


def _make_client() -> TestClient:
    with patch("app.db.client.create_client", return_value=MagicMock()):
        from app.main import app
        return TestClient(app)


# --- GET /sources ---

def test_list_sources_returns_200() -> None:
    with patch("app.routers.sources.repo.find_all", return_value=[]):
        c = _make_client()
        resp = c.get("/sources")
        assert resp.status_code == 200


def test_list_sources_envelope() -> None:
    with patch("app.routers.sources.repo.find_all", return_value=[_source()]):
        c = _make_client()
        data = c.get("/sources").json()
        assert data["success"] is True
        assert isinstance(data["data"], list)
        assert len(data["data"]) == 1


def test_list_sources_empty() -> None:
    with patch("app.routers.sources.repo.find_all", return_value=[]):
        c = _make_client()
        data = c.get("/sources").json()
        assert data["data"] == []


def test_list_sources_item_fields() -> None:
    with patch("app.routers.sources.repo.find_all", return_value=[_source()]):
        c = _make_client()
        item = c.get("/sources").json()["data"][0]
        for field in ("id", "name", "url", "type", "category", "priority", "status"):
            assert field in item


# --- POST /sources ---

def test_create_source_returns_201() -> None:
    src = _source()
    with patch("app.routers.sources.repo.create", return_value=src):
        c = _make_client()
        resp = c.post("/sources", json={
            "name": "arXiv cs.AI",
            "url": "https://export.arxiv.org/rss/cs.AI",
            "type": "rss",
            "category": "research",
            "priority": "high",
            "fetch_config": {"adapter": "arxiv"},
        })
        assert resp.status_code == 201


def test_create_source_returns_envelope() -> None:
    src = _source()
    with patch("app.routers.sources.repo.create", return_value=src):
        c = _make_client()
        data = c.post("/sources", json={
            "name": "arXiv cs.AI",
            "url": "https://export.arxiv.org/rss/cs.AI",
            "type": "rss",
            "category": "research",
            "priority": "high",
        }).json()
        assert data["success"] is True
        assert data["data"]["name"] == "arXiv cs.AI"


def test_create_source_missing_required_field_returns_422() -> None:
    c = _make_client()
    resp = c.post("/sources", json={"name": "Test"})
    assert resp.status_code == 422


def test_create_source_invalid_type_returns_422() -> None:
    c = _make_client()
    resp = c.post("/sources", json={
        "name": "Test", "url": "https://example.com",
        "type": "graphql", "category": "research", "priority": "high",
    })
    assert resp.status_code == 422


def test_create_source_unknown_adapter_returns_422() -> None:
    c = _make_client()
    resp = c.post("/sources", json={
        "name": "Test", "url": "https://example.com",
        "type": "rss", "category": "research", "priority": "high",
        "fetch_config": {"adapter": "unknown_adapter"},
    })
    assert resp.status_code == 422


# --- PATCH /sources/{id} ---

def test_update_source_returns_200() -> None:
    src = _source()
    source_id = str(src.id)
    with patch("app.routers.sources.repo.update", return_value=src):
        c = _make_client()
        resp = c.patch(f"/sources/{source_id}", json={"name": "Updated"})
        assert resp.status_code == 200


def test_update_source_returns_404_when_not_found() -> None:
    with patch("app.routers.sources.repo.update", return_value=None):
        c = _make_client()
        resp = c.patch(f"/sources/{uuid4()}", json={"name": "Updated"})
        assert resp.status_code == 404


def test_update_source_empty_body_returns_422() -> None:
    c = _make_client()
    resp = c.patch(f"/sources/{uuid4()}", json={})
    assert resp.status_code == 422


def test_update_source_invalid_uuid_returns_422() -> None:
    c = _make_client()
    resp = c.patch("/sources/not-a-uuid", json={"name": "X"})
    assert resp.status_code == 422


# --- POST /sources/{id}/retire ---

def test_retire_source_returns_200() -> None:
    src = _source()
    source_id = str(src.id)
    retired = Source(**{**src.model_dump(), "status": "inactive"})
    with patch("app.routers.sources.repo.update", return_value=retired):
        c = _make_client()
        resp = c.post(f"/sources/{source_id}/retire")
        assert resp.status_code == 200


def test_retire_source_returns_404() -> None:
    with patch("app.routers.sources.repo.update", return_value=None):
        c = _make_client()
        resp = c.post(f"/sources/{uuid4()}/retire")
        assert resp.status_code == 404


def test_retire_source_sets_status_inactive() -> None:
    src = _source()
    source_id = str(src.id)
    retired = Source(**{**src.model_dump(), "status": "inactive"})
    with patch("app.routers.sources.repo.update", return_value=retired) as mock_update:
        c = _make_client()
        c.post(f"/sources/{source_id}/retire")
    _, kwargs_or_args = mock_update.call_args
    # update called with {"status": "inactive"}
    update_data = mock_update.call_args[0][1]
    assert update_data == {"status": "inactive"}


# --- POST /sources/{id}/reactivate ---

def test_reactivate_source_returns_200() -> None:
    src = _source()
    source_id = str(src.id)
    with patch("app.routers.sources.repo.update", return_value=src):
        c = _make_client()
        resp = c.post(f"/sources/{source_id}/reactivate")
        assert resp.status_code == 200


def test_reactivate_source_returns_404() -> None:
    with patch("app.routers.sources.repo.update", return_value=None):
        c = _make_client()
        resp = c.post(f"/sources/{uuid4()}/reactivate")
        assert resp.status_code == 404


def test_reactivate_source_clears_failures() -> None:
    src = _source()
    source_id = str(src.id)
    with patch("app.routers.sources.repo.update", return_value=src) as mock_update:
        c = _make_client()
        c.post(f"/sources/{source_id}/reactivate")
    update_data = mock_update.call_args[0][1]
    assert update_data["status"] == "active"
    assert update_data["consecutive_failures"] == 0
    assert update_data["last_error"] is None


# --- DELETE /sources/{id} ---

def test_delete_source_returns_204() -> None:
    src = _source()
    source_id = str(src.id)
    with patch("app.routers.sources.repo.find_by_id", return_value=src), \
         patch("app.routers.sources.repo.has_items", return_value=False), \
         patch("app.routers.sources.repo.delete"):
        c = _make_client()
        resp = c.delete(f"/sources/{source_id}")
        assert resp.status_code == 204


def test_delete_source_returns_404_when_not_found() -> None:
    with patch("app.routers.sources.repo.find_by_id", return_value=None):
        c = _make_client()
        resp = c.delete(f"/sources/{uuid4()}")
        assert resp.status_code == 404


def test_delete_source_returns_409_when_has_items() -> None:
    src = _source()
    source_id = str(src.id)
    with patch("app.routers.sources.repo.find_by_id", return_value=src), \
         patch("app.routers.sources.repo.has_items", return_value=True):
        c = _make_client()
        resp = c.delete(f"/sources/{source_id}")
        assert resp.status_code == 409


def test_delete_source_409_message_mentions_retire() -> None:
    src = _source()
    source_id = str(src.id)
    with patch("app.routers.sources.repo.find_by_id", return_value=src), \
         patch("app.routers.sources.repo.has_items", return_value=True):
        c = _make_client()
        detail = c.delete(f"/sources/{source_id}").json()["detail"]
        assert "retire" in detail.lower()


def test_delete_source_invalid_uuid_returns_422() -> None:
    c = _make_client()
    resp = c.delete("/sources/not-a-uuid")
    assert resp.status_code == 422
