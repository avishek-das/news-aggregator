"""TDD: Source model validation tests."""
import pytest
from uuid import uuid4
from datetime import datetime, timezone
from pydantic import ValidationError
from app.models.source import (
    Source, SourceResponse, SourceCreateRequest, SourceUpdateRequest,
    SourcesListResponse, SourceSingleResponse,
)


def _source_row() -> dict:
    return {
        "id": str(uuid4()),
        "name": "arXiv cs.AI",
        "url": "https://export.arxiv.org/rss/cs.AI",
        "type": "rss",
        "category": "research",
        "priority": "high",
        "status": "active",
        "fetch_config": {"adapter": "arxiv"},
        "last_fetched_at": None,
        "last_error": None,
        "consecutive_failures": 0,
        "updated_at": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


# --- Source (DB model) ---

def test_source_parses_from_row() -> None:
    source = Source(**_source_row())
    assert source.name == "arXiv cs.AI"
    assert source.status == "active"


def test_source_is_frozen() -> None:
    source = Source(**_source_row())
    with pytest.raises(Exception):
        source.name = "changed"  # type: ignore[misc]


# --- SourceResponse ---

def test_source_response_parses_valid_literals() -> None:
    row = _source_row()
    resp = SourceResponse(**row)
    assert resp.type == "rss"
    assert resp.category == "research"
    assert resp.priority == "high"
    assert resp.status == "active"


def test_source_response_rejects_invalid_type() -> None:
    row = {**_source_row(), "type": "graphql"}
    with pytest.raises(ValidationError):
        SourceResponse(**row)


def test_source_response_rejects_invalid_category() -> None:
    row = {**_source_row(), "category": "sports"}
    with pytest.raises(ValidationError):
        SourceResponse(**row)


def test_source_response_rejects_invalid_priority() -> None:
    row = {**_source_row(), "priority": "critical"}
    with pytest.raises(ValidationError):
        SourceResponse(**row)


def test_source_response_rejects_invalid_status() -> None:
    row = {**_source_row(), "status": "deleted"}
    with pytest.raises(ValidationError):
        SourceResponse(**row)


# --- SourceCreateRequest ---

def test_create_request_valid() -> None:
    req = SourceCreateRequest(
        name="HN",
        url="https://news.ycombinator.com/rss",
        type="rss",
        category="community",
        priority="medium",
        fetch_config={"adapter": "hackernews"},
    )
    assert req.name == "HN"


def test_create_request_defaults_fetch_config() -> None:
    req = SourceCreateRequest(
        name="HN", url="https://hn.com", type="rss",
        category="community", priority="medium",
    )
    assert req.fetch_config == {}


def test_create_request_rejects_unknown_adapter() -> None:
    with pytest.raises(ValidationError, match="Unknown adapter"):
        SourceCreateRequest(
            name="HN", url="https://hn.com", type="rss",
            category="community", priority="medium",
            fetch_config={"adapter": "unknown_adapter"},
        )


def test_create_request_allows_known_adapters() -> None:
    for adapter in ("arxiv", "hackernews", "reddit", "youtube", "huggingface"):
        req = SourceCreateRequest(
            name="Test", url="https://example.com", type="api",
            category="research", priority="low",
            fetch_config={"adapter": adapter},
        )
        assert req.fetch_config["adapter"] == adapter


def test_create_request_allows_empty_fetch_config() -> None:
    req = SourceCreateRequest(
        name="Test", url="https://example.com", type="rss",
        category="media", priority="low",
        fetch_config={},
    )
    assert req.fetch_config == {}


# --- SourceUpdateRequest ---

def test_update_request_partial_valid() -> None:
    req = SourceUpdateRequest(name="New Name")
    assert req.name == "New Name"
    assert req.url is None


def test_update_request_rejects_all_none() -> None:
    with pytest.raises(ValidationError, match="At least one field"):
        SourceUpdateRequest()


def test_update_request_allows_status_change() -> None:
    req = SourceUpdateRequest(status="inactive")
    assert req.status == "inactive"


def test_update_request_rejects_invalid_status() -> None:
    with pytest.raises(ValidationError):
        SourceUpdateRequest(status="banned")


def test_update_request_validates_adapter_in_fetch_config() -> None:
    with pytest.raises(ValidationError, match="Unknown adapter"):
        SourceUpdateRequest(fetch_config={"adapter": "bad_adapter"})


def test_update_request_allows_fetch_config_without_adapter() -> None:
    req = SourceUpdateRequest(fetch_config={"max_results": 50})
    assert req.fetch_config == {"max_results": 50}


# --- Envelope models ---

def test_sources_list_response_success() -> None:
    row = _source_row()
    resp = SourcesListResponse(success=True, data=[SourceResponse(**row)])
    assert resp.success is True
    assert len(resp.data) == 1


def test_source_single_response_with_error() -> None:
    resp = SourceSingleResponse(success=False, data=None, error="Not found")
    assert resp.success is False
    assert resp.error == "Not found"
    assert resp.data is None
