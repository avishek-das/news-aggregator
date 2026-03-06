import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from app.adapters.lab_blogs import LabBlogsAdapter

FIXTURES = Path(__file__).parent.parent / "fixtures"
XML = (FIXTURES / "lab_blog_rss.xml").read_text()

FEEDS = [
    {"name": "OpenAI", "url": "https://openai.com/blog/rss.xml"},
    {"name": "Anthropic", "url": "https://www.anthropic.com/rss.xml"},
]


def make_adapter():
    return LabBlogsAdapter(source_id="test", fetch_config={"feeds": FEEDS})


class TestLabBlogsAdapter:
    def test_parse_returns_items(self):
        items = make_adapter()._parse(XML, "OpenAI")
        assert len(items) == 2

    def test_category_is_research(self):
        items = make_adapter()._parse(XML, "OpenAI")
        assert all(i.category == "research" for i in items)

    def test_lab_name_in_metadata(self):
        items = make_adapter()._parse(XML, "OpenAI")
        assert all(i.raw_metadata.get("lab") == "OpenAI" for i in items)

    @pytest.mark.asyncio
    async def test_fetch_iterates_all_feeds(self):
        adapter = make_adapter()
        mock_response = MagicMock(raise_for_status=MagicMock(), text=XML)
        with patch("httpx.AsyncClient") as cls:
            mc = AsyncMock()
            mc.__aenter__ = AsyncMock(return_value=mc)
            mc.__aexit__ = AsyncMock(return_value=None)
            mc.get = AsyncMock(return_value=mock_response)
            cls.return_value = mc
            items = await adapter.fetch()
        assert mc.get.call_count == 2
        assert len(items) == 4  # 2 items × 2 feeds

    @pytest.mark.asyncio
    async def test_handles_feed_failure_gracefully(self):
        adapter = make_adapter()
        good = MagicMock(raise_for_status=MagicMock(), text=XML)
        bad = MagicMock()
        bad.raise_for_status.side_effect = Exception("404")
        with patch("httpx.AsyncClient") as cls:
            mc = AsyncMock()
            mc.__aenter__ = AsyncMock(return_value=mc)
            mc.__aexit__ = AsyncMock(return_value=None)
            mc.get = AsyncMock(side_effect=[bad, good])
            cls.return_value = mc
            items = await adapter.fetch()
        assert len(items) == 2  # only good feed items
