import pytest
import json
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from app.adapters.huggingface import HuggingFaceAdapter

FIXTURES = Path(__file__).parent.parent / "fixtures"
DATA = json.loads((FIXTURES / "huggingface_daily_papers.json").read_text())


def make_adapter():
    return HuggingFaceAdapter(source_id="test", fetch_config={})


class TestHuggingFaceAdapter:
    def test_parse_returns_correct_count(self):
        assert len(make_adapter()._parse(DATA)) == 2

    def test_title_extracted(self):
        items = make_adapter()._parse(DATA)
        assert "FlashAttention" in items[0].title

    def test_url_points_to_hf_papers(self):
        items = make_adapter()._parse(DATA)
        assert "huggingface.co/papers/" in items[0].url

    def test_excerpt_from_summary(self):
        items = make_adapter()._parse(DATA)
        assert "FlashAttention" in items[0].excerpt

    def test_category_is_research(self):
        items = make_adapter()._parse(DATA)
        assert all(i.category == "research" for i in items)

    def test_authors_in_metadata(self):
        items = make_adapter()._parse(DATA)
        assert "Tri Dao" in items[0].raw_metadata["authors"]

    def test_published_at_parsed(self):
        items = make_adapter()._parse(DATA)
        assert items[0].published_at is not None
        assert items[0].published_at.year == 2026

    @pytest.mark.asyncio
    async def test_fetch_calls_correct_url(self):
        adapter = make_adapter()
        mock_response = MagicMock(raise_for_status=MagicMock())
        mock_response.json = MagicMock(return_value=DATA)
        with patch("httpx.AsyncClient") as cls:
            mc = AsyncMock()
            mc.__aenter__ = AsyncMock(return_value=mc)
            mc.__aexit__ = AsyncMock(return_value=None)
            mc.get = AsyncMock(return_value=mock_response)
            cls.return_value = mc
            await adapter.fetch()
        assert "huggingface.co" in mc.get.call_args.args[0]
