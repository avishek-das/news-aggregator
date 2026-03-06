"""TDD: SourceRepository tests."""
from unittest.mock import MagicMock, patch
from uuid import uuid4
import pytest


def make_mock_client(rows: list[dict]) -> MagicMock:
    mock = MagicMock()
    mock.table.return_value.select.return_value.eq.return_value.execute.return_value.data = rows
    mock.table.return_value.update.return_value.eq.return_value.execute.return_value.data = []
    mock.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = rows[0] if rows else {}
    return mock


def _source_row(status: str = "active", failures: int = 0) -> dict:
    return {
        "id": str(uuid4()), "name": "arXiv", "url": "https://example.com",
        "type": "api", "category": "research", "priority": "high",
        "status": status, "fetch_config": {"adapter": "arxiv"},
        "last_fetched_at": None, "last_error": None,
        "consecutive_failures": failures, "created_at": "2026-01-01T00:00:00+00:00",
    }


def test_find_active_returns_only_active_sources() -> None:
    rows = [_source_row("active")]
    mock_client = make_mock_client(rows)
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import find_active
        sources = find_active()
        assert len(sources) == 1
        assert sources[0].status == "active"


def test_find_active_returns_source_objects() -> None:
    from app.models.source import Source
    rows = [_source_row()]
    mock_client = make_mock_client(rows)
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import find_active
        sources = find_active()
        assert isinstance(sources[0], Source)


def test_record_success_resets_failures() -> None:
    mock_client = MagicMock()
    source_id = str(uuid4())
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import record_success
        record_success(source_id, item_count=5)
    call_args = mock_client.table.return_value.update.call_args
    update_data = call_args[0][0]
    assert update_data["consecutive_failures"] == 0
    assert update_data["last_error"] is None


def test_record_failure_increments_failures() -> None:
    source_id = str(uuid4())
    row = _source_row(failures=1)
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = row
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import record_failure
        record_failure(source_id, "timeout error")
    update_call = mock_client.table.return_value.update.call_args[0][0]
    assert update_call["consecutive_failures"] == 2
    assert update_call["last_error"] == "timeout error"


def test_record_failure_flags_after_three() -> None:
    source_id = str(uuid4())
    row = _source_row(failures=2)
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = row
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import record_failure
        record_failure(source_id, "error")
    update_call = mock_client.table.return_value.update.call_args[0][0]
    assert update_call["status"] == "flagged"


def test_record_failure_does_not_flag_before_three() -> None:
    source_id = str(uuid4())
    row = _source_row(failures=0)
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = row
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import record_failure
        record_failure(source_id, "error")
    update_call = mock_client.table.return_value.update.call_args[0][0]
    assert "status" not in update_call or update_call.get("status") != "flagged"


def _source_row_full(source_id: str | None = None) -> dict:
    return {
        "id": source_id or str(uuid4()),
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
        "created_at": "2026-01-01T00:00:00+00:00",
    }


# --- find_all ---

def test_find_all_returns_list_of_sources() -> None:
    row = _source_row_full()
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.order.return_value.execute.return_value.data = [row]
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import find_all
        results = find_all()
        assert len(results) == 1
        assert results[0].name == "arXiv cs.AI"


def test_find_all_orders_by_name() -> None:
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.order.return_value.execute.return_value.data = []
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import find_all
        find_all()
    order_call = mock_client.table.return_value.select.return_value.order.call_args
    assert "name" in str(order_call)


def test_find_all_empty() -> None:
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.order.return_value.execute.return_value.data = []
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import find_all
        assert find_all() == []


# --- find_by_id ---

def test_find_by_id_returns_source() -> None:
    source_id = str(uuid4())
    row = _source_row_full(source_id)
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [row]
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import find_by_id
        result = find_by_id(source_id)
        assert result is not None
        assert str(result.id) == source_id


def test_find_by_id_returns_none_when_not_found() -> None:
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import find_by_id
        assert find_by_id(str(uuid4())) is None


# --- create ---

def test_create_inserts_and_returns_source() -> None:
    row = _source_row_full()
    mock_client = MagicMock()
    mock_client.table.return_value.insert.return_value.execute.return_value.data = [row]
    data = {
        "name": "arXiv cs.AI", "url": "https://export.arxiv.org/rss/cs.AI",
        "type": "rss", "category": "research", "priority": "high",
        "fetch_config": {"adapter": "arxiv"},
    }
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import create
        result = create(data)
        assert result.name == "arXiv cs.AI"


def test_create_passes_data_to_insert() -> None:
    row = _source_row_full()
    mock_client = MagicMock()
    mock_client.table.return_value.insert.return_value.execute.return_value.data = [row]
    data = {"name": "Test", "url": "https://test.com", "type": "rss",
            "category": "media", "priority": "low", "fetch_config": {}}
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import create
        create(data)
    insert_call = mock_client.table.return_value.insert.call_args[0][0]
    assert insert_call == data


# --- update ---

def test_update_returns_updated_source() -> None:
    source_id = str(uuid4())
    row = {**_source_row_full(source_id), "name": "Updated"}
    mock_client = MagicMock()
    mock_client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [row]
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import update
        result = update(source_id, {"name": "Updated"})
        assert result is not None
        assert result.name == "Updated"


def test_update_returns_none_when_not_found() -> None:
    mock_client = MagicMock()
    mock_client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = []
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import update
        result = update(str(uuid4()), {"name": "Ghost"})
        assert result is None


def test_update_injects_updated_at() -> None:
    source_id = str(uuid4())
    row = _source_row_full(source_id)
    mock_client = MagicMock()
    mock_client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [row]
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import update
        update(source_id, {"name": "New"})
    update_payload = mock_client.table.return_value.update.call_args[0][0]
    assert "updated_at" in update_payload


# --- delete ---

def test_delete_calls_supabase_delete() -> None:
    source_id = str(uuid4())
    mock_client = MagicMock()
    mock_client.table.return_value.delete.return_value.eq.return_value.execute.return_value.data = []
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import delete
        delete(source_id)
    mock_client.table.return_value.delete.assert_called_once()


# --- has_items ---

def test_has_items_returns_true_when_items_exist() -> None:
    source_id = str(uuid4())
    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.count = 1
    mock_client.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = mock_result
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import has_items
        assert has_items(source_id) is True


def test_has_items_returns_false_when_no_items() -> None:
    source_id = str(uuid4())
    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.count = 0
    mock_client.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = mock_result
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import has_items
        assert has_items(source_id) is False


def test_has_items_handles_none_count() -> None:
    source_id = str(uuid4())
    mock_client = MagicMock()
    mock_result = MagicMock()
    mock_result.count = None
    mock_client.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = mock_result
    with patch("app.repositories.sources.get_client", return_value=mock_client):
        from app.repositories.sources import has_items
        assert has_items(source_id) is False
