"""TDD: arXiv adapter tests."""
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime


FIXTURE = Path(__file__).parent.parent / "fixtures" / "arxiv_response.xml"


def test_parse_returns_correct_count() -> None:
    from app.adapters.arxiv import ArxivAdapter
    xml = FIXTURE.read_text()
    adapter = ArxivAdapter(source_id="test-id", fetch_config={})
    items = adapter._parse(xml)
    assert len(items) == 2


def test_title_is_stripped() -> None:
    from app.adapters.arxiv import ArxivAdapter
    xml = FIXTURE.read_text()
    adapter = ArxivAdapter(source_id="test-id", fetch_config={})
    items = adapter._parse(xml)
    assert items[0].title == "Large Language Models: A Survey"


def test_excerpt_from_summary() -> None:
    from app.adapters.arxiv import ArxivAdapter
    xml = FIXTURE.read_text()
    items = ArxivAdapter(source_id="x", fetch_config={})._parse(xml)
    assert "survey" in items[0].excerpt.lower()


def test_url_from_id_element() -> None:
    from app.adapters.arxiv import ArxivAdapter
    xml = FIXTURE.read_text()
    items = ArxivAdapter(source_id="x", fetch_config={})._parse(xml)
    assert "arxiv.org/abs/2401.00001" in items[0].url


def test_category_is_research() -> None:
    from app.adapters.arxiv import ArxivAdapter
    xml = FIXTURE.read_text()
    items = ArxivAdapter(source_id="x", fetch_config={})._parse(xml)
    assert all(i.category == "research" for i in items)


def test_authors_in_raw_metadata() -> None:
    from app.adapters.arxiv import ArxivAdapter
    xml = FIXTURE.read_text()
    items = ArxivAdapter(source_id="x", fetch_config={})._parse(xml)
    assert "authors" in items[0].raw_metadata
    assert "Jane Doe" in items[0].raw_metadata["authors"]


def test_published_at_parsed() -> None:
    from app.adapters.arxiv import ArxivAdapter
    xml = FIXTURE.read_text()
    items = ArxivAdapter(source_id="x", fetch_config={})._parse(xml)
    assert isinstance(items[0].published_at, datetime)


@pytest.mark.asyncio
async def test_fetch_calls_api() -> None:
    from app.adapters.arxiv import ArxivAdapter
    mock_response = MagicMock()
    mock_response.text = FIXTURE.read_text()
    mock_response.raise_for_status = MagicMock()
    with patch("httpx.AsyncClient") as mock_http:
        mock_http.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        adapter = ArxivAdapter(source_id="x", fetch_config={}, url="https://export.arxiv.org/api/query")
        items = await adapter.fetch()
        assert len(items) == 2
