import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from app.adapters.papers_with_code import PapersWithCodeAdapter

FIXTURES = Path(__file__).parent.parent / "fixtures"
XML = (FIXTURES / "papers_with_code_rss.xml").read_text()


def make_adapter():
    return PapersWithCodeAdapter(source_id="test", fetch_config={})


class TestPapersWithCodeAdapter:
    def test_parse_returns_items(self):
        assert len(make_adapter()._parse(XML)) == 2

    def test_category_is_research(self):
        items = make_adapter()._parse(XML)
        assert all(i.category == "research" for i in items)

    def test_title_extracted(self):
        items = make_adapter()._parse(XML)
        assert "Efficient Transformers" in items[0].title

    def test_url_extracted(self):
        items = make_adapter()._parse(XML)
        assert "paperswithcode.com" in items[0].url

    @pytest.mark.asyncio
    async def test_fetch_calls_rss_url(self):
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
        assert "paperswithcode" in mc.get.call_args.args[0]
