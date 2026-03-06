"""TDD: Pydantic model tests."""
from datetime import datetime, timezone
import uuid
from app.models.item import ItemResponse, ItemsListResponse, Meta
from app.models.source import Source


def test_item_response_defaults() -> None:
    item = ItemResponse(
        id=uuid.uuid4(),
        source_id=uuid.uuid4(),
        source_name="arXiv cs.AI",
        title="Test Paper",
        url="https://arxiv.org/abs/test",
        category="research",
        created_at=datetime.now(timezone.utc),
    )
    assert item.is_read is False
    assert item.summary is None
    assert item.is_paywalled is False


def test_item_response_serialization() -> None:
    item = ItemResponse(
        id=uuid.uuid4(),
        source_id=uuid.uuid4(),
        source_name="Hacker News",
        title="AI Story",
        url="https://example.com",
        category="community",
        created_at=datetime.now(timezone.utc),
    )
    d = item.model_dump()
    assert "id" in d and "source_name" in d and "is_read" in d


def test_items_meta_fields() -> None:
    meta = Meta(total=100, limit=10, offset=0)
    assert meta.total == 100
    assert meta.limit == 10
    assert meta.offset == 0


def test_items_list_response_shape() -> None:
    resp = ItemsListResponse(success=True, data=[], error=None, meta=Meta(total=0, limit=10, offset=0))
    assert resp.success is True
    assert resp.data == []


def test_source_model_fields() -> None:
    source = Source(
        id=uuid.uuid4(),
        name="arXiv cs.AI",
        url="https://export.arxiv.org/api/query",
        type="api",
        category="research",
        priority="high",
        status="active",
        fetch_config={"adapter": "arxiv"},
        consecutive_failures=0,
    )
    assert source.status == "active"
    assert source.fetch_config["adapter"] == "arxiv"
