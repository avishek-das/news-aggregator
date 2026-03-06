import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from app.adapters.lobsters import LobstersAdapter

FIXTURES = Path(__file__).parent.parent / "fixtures"
XML = (FIXTURES / "lobsters_rss.xml").read_text()


def make_adapter(tags=None):
    return LobstersAdapter(
        source_id="test",
        fetch_config={"tags": tags or ["ai", "llm"]},
    )


class TestLobstersAdapter:
    def test_parse_returns_items(self):
        items = make_adapter()._parse(XML)
        assert len(items) == 3  # fixture has 3 raw items (dup not yet removed in _parse)

    def test_category_is_community(self):
        items = make_adapter()._parse(XML)
        assert all(i.category == "community" for i in items)

    @pytest.mark.asyncio
    async def test_fetch_deduplicates_by_url(self):
        adapter = make_adapter(["ai"])
        mock_response = MagicMock(raise_for_status=MagicMock(), text=XML)
        with patch("httpx.AsyncClient") as cls:
            mc = AsyncMock()
            mc.__aenter__ = AsyncMock(return_value=mc)
            mc.__aexit__ = AsyncMock(return_value=None)
            mc.get = AsyncMock(return_value=mock_response)
            cls.return_value = mc
            items = await adapter.fetch()
        # 3 items in fixture but 1 duplicate URL → 2 unique
        assert len(items) == 2

    @pytest.mark.asyncio
    async def test_fetch_merges_multiple_tags(self):
        adapter = make_adapter(["ai", "llm"])
        mock_response = MagicMock(raise_for_status=MagicMock(), text=XML)
        with patch("httpx.AsyncClient") as cls:
            mc = AsyncMock()
            mc.__aenter__ = AsyncMock(return_value=mc)
            mc.__aexit__ = AsyncMock(return_value=None)
            mc.get = AsyncMock(return_value=mock_response)
            cls.return_value = mc
            await adapter.fetch()
        assert mc.get.call_count == 2
