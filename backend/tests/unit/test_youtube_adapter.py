import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from app.adapters.youtube import YouTubeAdapter

FIXTURES = Path(__file__).parent.parent / "fixtures"
XML = (FIXTURES / "youtube_atom.xml").read_text()

CHANNELS = [
    {"name": "Two Minute Papers", "channel_id": "UCbfYPyITQ-7l4upoX8nvctg"},
    {"name": "Yannic Kilcher", "channel_id": "UCZHmQk67mSJgfCCTn7xBfew"},
]


def make_adapter():
    return YouTubeAdapter(source_id="test", fetch_config={"channels": CHANNELS})


class TestYouTubeAdapter:
    def test_parse_returns_items(self):
        items = make_adapter()._parse(XML, "Two Minute Papers")
        assert len(items) == 2

    def test_category_is_media(self):
        items = make_adapter()._parse(XML, "Two Minute Papers")
        assert all(i.category == "media" for i in items)

    def test_url_is_youtube_watch_link(self):
        items = make_adapter()._parse(XML, "Two Minute Papers")
        assert all("youtube.com/watch" in i.url for i in items)

    def test_channel_name_in_metadata(self):
        items = make_adapter()._parse(XML, "Two Minute Papers")
        assert all(i.raw_metadata["channel_name"] == "Two Minute Papers" for i in items)

    def test_video_id_in_metadata(self):
        items = make_adapter()._parse(XML, "Two Minute Papers")
        assert items[0].raw_metadata["video_id"] == "abc123xyz"

    @pytest.mark.asyncio
    async def test_fetch_iterates_channels(self):
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
        assert len(items) == 4  # 2 items × 2 channels
