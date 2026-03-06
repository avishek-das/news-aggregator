import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from app.adapters.arxiv_extra import ArxivExtraAdapter

FIXTURES = Path(__file__).parent.parent / "fixtures"
ARXIV_XML = (FIXTURES / "arxiv_response.xml").read_text()


def make_adapter(categories=None):
    return ArxivExtraAdapter(
        source_id="test",
        fetch_config={"categories": categories or ["cs.LG", "cs.CL"], "max_results": 10},
    )


class TestArxivExtraAdapter:
    def test_parse_reuses_parent_logic(self):
        adapter = make_adapter()
        items = adapter._parse(ARXIV_XML)
        assert len(items) == 2
        assert items[0].category == "research"

    @pytest.mark.asyncio
    async def test_fetch_calls_url_per_category(self):
        adapter = make_adapter(["cs.LG", "cs.CL"])
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.text = ARXIV_XML
        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client_cls.return_value = mock_client
            await adapter.fetch()
        assert mock_client.get.call_count == 2
        urls = [str(c.args[0]) for c in mock_client.get.call_args_list]
        assert any("cs.LG" in u for u in urls)
        assert any("cs.CL" in u for u in urls)

    @pytest.mark.asyncio
    async def test_merges_and_deduplicates_results(self):
        adapter = make_adapter(["cs.LG", "cs.CL"])
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.text = ARXIV_XML  # same fixture → same URLs → deduped
        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client_cls.return_value = mock_client
            items = await adapter.fetch()
        # 2 unique items despite 2 categories returning same fixture
        assert len(items) == 2
