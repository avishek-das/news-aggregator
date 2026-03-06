import pytest
import json
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from app.adapters.openreview import OpenReviewAdapter

FIXTURES = Path(__file__).parent.parent / "fixtures"
DATA = json.loads((FIXTURES / "openreview_response.json").read_text())


def make_adapter():
    return OpenReviewAdapter(
        source_id="test",
        fetch_config={"venues": ["ICML.cc/2025/Conference"]},
    )


class TestOpenReviewAdapter:
    def test_parse_returns_correct_count(self):
        assert len(make_adapter()._parse(DATA)) == 2

    def test_title_extracted(self):
        items = make_adapter()._parse(DATA)
        assert "Attention Is All You Need" in items[0].title

    def test_url_points_to_openreview(self):
        items = make_adapter()._parse(DATA)
        assert "openreview.net/forum?id=AbCdEfGhIj" in items[0].url

    def test_excerpt_from_abstract(self):
        items = make_adapter()._parse(DATA)
        assert "transformer" in items[0].excerpt

    def test_missing_abstract_returns_empty_excerpt(self):
        items = make_adapter()._parse(DATA)
        assert items[1].excerpt == ""

    def test_category_is_research(self):
        items = make_adapter()._parse(DATA)
        assert all(i.category == "research" for i in items)

    def test_authors_in_metadata(self):
        items = make_adapter()._parse(DATA)
        assert "Alice Researcher" in items[0].raw_metadata["authors"]

    @pytest.mark.asyncio
    async def test_fetch_iterates_venues(self):
        adapter = OpenReviewAdapter(
            source_id="test",
            fetch_config={"venues": ["ICML.cc/2025", "NeurIPS.cc/2025"]},
        )
        mock_response = MagicMock(raise_for_status=MagicMock())
        mock_response.json = MagicMock(return_value=DATA)
        with patch("httpx.AsyncClient") as cls:
            mc = AsyncMock()
            mc.__aenter__ = AsyncMock(return_value=mc)
            mc.__aexit__ = AsyncMock(return_value=None)
            mc.get = AsyncMock(return_value=mock_response)
            cls.return_value = mc
            await adapter.fetch()
        assert mc.get.call_count == 2
