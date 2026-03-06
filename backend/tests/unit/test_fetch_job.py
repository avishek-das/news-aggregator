"""TDD: Daily fetch job tests."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from app.adapters.base import RawItem
from datetime import datetime, timezone


def _make_source(adapter: str = "arxiv") -> MagicMock:
    s = MagicMock()
    s.id = str(uuid4())
    s.fetch_config = {"adapter": adapter, "url": "https://example.com"}
    return s


def _make_raw_item() -> RawItem:
    return RawItem(title="T", url="https://x.com", excerpt="e",
                   published_at=datetime.now(timezone.utc), category="research")


@pytest.mark.asyncio
async def test_fetch_job_records_success() -> None:
    source = _make_source()
    with (
        patch("app.jobs.fetch_sources.find_active", return_value=[source]),
        patch("app.jobs.fetch_sources.get_adapter") as mock_registry,
        patch("app.jobs.fetch_sources.upsert", return_value=2),
        patch("app.jobs.fetch_sources.record_success") as mock_success,
        patch("app.jobs.fetch_sources.record_failure"),
    ):
        mock_adapter = AsyncMock()
        mock_adapter.fetch = AsyncMock(return_value=[_make_raw_item(), _make_raw_item()])
        mock_registry.return_value = mock_adapter
        from app.jobs.fetch_sources import run_fetch_job
        await run_fetch_job()
        mock_success.assert_called_once_with(source.id, 2)


@pytest.mark.asyncio
async def test_fetch_job_records_failure_on_error() -> None:
    source = _make_source()
    with (
        patch("app.jobs.fetch_sources.find_active", return_value=[source]),
        patch("app.jobs.fetch_sources.get_adapter") as mock_registry,
        patch("app.jobs.fetch_sources.record_success"),
        patch("app.jobs.fetch_sources.record_failure") as mock_failure,
    ):
        mock_adapter = AsyncMock()
        mock_adapter.fetch = AsyncMock(side_effect=Exception("timeout"))
        mock_registry.return_value = mock_adapter
        from app.jobs.fetch_sources import run_fetch_job
        await run_fetch_job()
        mock_failure.assert_called_once_with(source.id, "timeout")


@pytest.mark.asyncio
async def test_fetch_job_continues_after_one_failure() -> None:
    s1, s2 = _make_source(), _make_source()
    success_calls = []
    with (
        patch("app.jobs.fetch_sources.find_active", return_value=[s1, s2]),
        patch("app.jobs.fetch_sources.get_adapter") as mock_registry,
        patch("app.jobs.fetch_sources.upsert", return_value=1),
        patch("app.jobs.fetch_sources.record_success", side_effect=lambda sid, c: success_calls.append(sid)),
        patch("app.jobs.fetch_sources.record_failure"),
    ):
        call_count = 0
        async def side_effect_fetch():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("first fails")
            return [_make_raw_item()]
        mock_adapter = AsyncMock()
        mock_adapter.fetch = side_effect_fetch
        mock_registry.return_value = mock_adapter
        from app.jobs.fetch_sources import run_fetch_job
        await run_fetch_job()
        assert len(success_calls) == 1  # second source succeeded


@pytest.mark.asyncio
async def test_fetch_job_skips_unknown_adapter() -> None:
    source = _make_source(adapter="unknown_xyz")
    with (
        patch("app.jobs.fetch_sources.find_active", return_value=[source]),
        patch("app.jobs.fetch_sources.record_failure") as mock_failure,
        patch("app.jobs.fetch_sources.record_success"),
    ):
        from app.jobs.fetch_sources import run_fetch_job
        await run_fetch_job()
        mock_failure.assert_called_once()
