import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from app.adapters.podcasts import PodcastsAdapter

FIXTURES = Path(__file__).parent.parent / "fixtures"
XML = (FIXTURES / "podcast_rss.xml").read_text()

FEEDS = [
    {"name": "Lex Fridman Podcast", "url": "https://lexfridman.com/feed/podcast/"},
]


def make_adapter():
    return PodcastsAdapter(source_id="test", fetch_config={"feeds": FEEDS})


class TestPodcastsAdapter:
    def test_parse_returns_items(self):
        items = make_adapter()._parse(XML, "Lex Fridman Podcast")
        assert len(items) == 2

    def test_category_is_media(self):
        items = make_adapter()._parse(XML, "Lex Fridman Podcast")
        assert all(i.category == "media" for i in items)

    def test_podcast_name_in_metadata(self):
        items = make_adapter()._parse(XML, "Lex Fridman Podcast")
        assert all(i.raw_metadata["podcast_name"] == "Lex Fridman Podcast" for i in items)

    def test_duration_in_metadata(self):
        items = make_adapter()._parse(XML, "Lex Fridman Podcast")
        assert items[0].raw_metadata["duration"] == "3:42:15"

    @pytest.mark.asyncio
    async def test_fetch_iterates_feed_urls(self):
        adapter = make_adapter()
        mock_response = MagicMock(raise_for_status=MagicMock(), text=XML)
        with patch("httpx.AsyncClient") as cls:
            mc = AsyncMock()
            mc.__aenter__ = AsyncMock(return_value=mc)
            mc.__aexit__ = AsyncMock(return_value=None)
            mc.get = AsyncMock(return_value=mock_response)
            cls.return_value = mc
            items = await adapter.fetch()
        assert len(items) == 2
