"""TDD: HackerNews adapter tests."""
import json
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime


FIXTURE = Path(__file__).parent.parent / "fixtures" / "hackernews_response.json"


def _parse(min_score: int = 10):
    from app.adapters.hackernews import HackerNewsAdapter
    data = json.loads(FIXTURE.read_text())
    adapter = HackerNewsAdapter(source_id="x", fetch_config={"min_score": min_score})
    return adapter._parse(data["hits"])


def test_filters_by_min_score() -> None:
    items = _parse(min_score=10)
    # fixture: scores 500, 3, 150 → score=3 filtered out
    assert len(items) == 2


def test_title_from_title_field() -> None:
    items = _parse()
    assert items[0].title == "GPT-4 Technical Report Released"


def test_url_from_url_field() -> None:
    items = _parse()
    assert items[0].url == "https://openai.com/gpt-4"


def test_url_fallback_to_hn_link() -> None:
    items = _parse()
    # third hit (objectID=12347) has null url → should use HN link
    hn_item = next(i for i in items if "Ask HN" in i.title)
    assert "news.ycombinator.com/item?id=12347" in hn_item.url


def test_excerpt_from_story_text() -> None:
    items = _parse()
    hn_item = next(i for i in items if "Ask HN" in i.title)
    assert "AI tools" in hn_item.excerpt


def test_category_is_community() -> None:
    items = _parse()
    assert all(i.category == "community" for i in items)


def test_published_at_parsed() -> None:
    items = _parse()
    assert isinstance(items[0].published_at, datetime)


def test_score_in_raw_metadata() -> None:
    items = _parse()
    assert items[0].raw_metadata["score"] == 500


@pytest.mark.asyncio
async def test_fetch_calls_algolia_api() -> None:
    from app.adapters.hackernews import HackerNewsAdapter
    mock_response = MagicMock()
    mock_response.json.return_value = json.loads(FIXTURE.read_text())
    mock_response.raise_for_status = MagicMock()
    with patch("httpx.AsyncClient") as mock_http:
        mock_http.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        adapter = HackerNewsAdapter(source_id="x", fetch_config={"min_score": 10})
        items = await adapter.fetch()
        assert len(items) == 2
