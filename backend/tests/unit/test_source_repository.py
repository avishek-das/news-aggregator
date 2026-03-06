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
