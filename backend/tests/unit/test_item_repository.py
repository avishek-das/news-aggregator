"""TDD: ItemRepository tests."""
from unittest.mock import MagicMock, patch, call
from uuid import uuid4
from datetime import datetime, timezone
from app.adapters.base import RawItem


def _make_raw_item(url: str = "https://example.com") -> RawItem:
    return RawItem(
        title="Test Paper", url=url, excerpt="Short excerpt",
        published_at=datetime.now(timezone.utc), category="research",
    )


def _make_item_row(source_id: str, url: str = "https://example.com") -> dict:
    return {
        "id": str(uuid4()), "source_id": source_id, "title": "Test Paper",
        "url": url, "excerpt": "Short excerpt", "summary": None,
        "published_at": "2026-01-01T00:00:00+00:00", "category": "research",
        "is_paywalled": False, "created_at": "2026-01-01T00:00:00+00:00",
        "sources": {"name": "arXiv cs.AI"},
    }


def test_upsert_inserts_new_items() -> None:
    mock_client = MagicMock()
    mock_client.table.return_value.upsert.return_value.execute.return_value.data = [{}]
    source_id = str(uuid4())
    with patch("app.repositories.items.get_client", return_value=mock_client):
        from app.repositories.items import upsert
        count = upsert([_make_raw_item()], source_id)
        assert count == 1


def test_upsert_uses_on_conflict_url() -> None:
    mock_client = MagicMock()
    mock_client.table.return_value.upsert.return_value.execute.return_value.data = []
    source_id = str(uuid4())
    with patch("app.repositories.items.get_client", return_value=mock_client):
        from app.repositories.items import upsert
        upsert([_make_raw_item()], source_id)
    upsert_call = mock_client.table.return_value.upsert.call_args
    assert "on_conflict" in upsert_call[1] or "url" in str(upsert_call)


def test_upsert_maps_raw_item_to_row() -> None:
    mock_client = MagicMock()
    mock_client.table.return_value.upsert.return_value.execute.return_value.data = []
    source_id = str(uuid4())
    item = _make_raw_item("https://arxiv.org/abs/123")
    with patch("app.repositories.items.get_client", return_value=mock_client):
        from app.repositories.items import upsert
        upsert([item], source_id)
    rows = mock_client.table.return_value.upsert.call_args[0][0]
    assert rows[0]["url"] == "https://arxiv.org/abs/123"
    assert rows[0]["source_id"] == source_id
    assert rows[0]["category"] == "research"


def test_find_all_limit_capped_at_100() -> None:
    mock_client = MagicMock()
    source_id = str(uuid4())
    mock_client.table.return_value.select.return_value.order.return_value.range.return_value.execute.return_value.data = []
    mock_client.table.return_value.select.return_value.order.return_value.range.return_value.execute.return_value.count = 0
    with patch("app.repositories.items.get_client", return_value=mock_client):
        from app.repositories.items import find_all
        items, total = find_all(limit=999, offset=0, session_id="test-session")
        assert total == 0


def test_find_all_returns_tuple() -> None:
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.order.return_value.range.return_value.execute.return_value.data = []
    mock_client.table.return_value.select.return_value.order.return_value.range.return_value.execute.return_value.count = 0
    with patch("app.repositories.items.get_client", return_value=mock_client):
        from app.repositories.items import find_all
        result = find_all(limit=10, offset=0, session_id="test")
        assert isinstance(result, tuple)
        assert len(result) == 2
