import pytest
import json
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from app.adapters.reddit import RedditAdapter

FIXTURES = Path(__file__).parent.parent / "fixtures"
DATA = json.loads((FIXTURES / "reddit_response.json").read_text())


def make_adapter(min_score=50):
    return RedditAdapter(
        source_id="test",
        fetch_config={"subreddits": ["MachineLearning"], "min_score": min_score},
    )


class TestRedditAdapter:
    def test_parse_filters_by_min_score(self):
        items = make_adapter(min_score=50)._parse(DATA, min_score=50)
        assert len(items) == 2  # score 500 and 200 pass; score 3 filtered

    def test_title_extracted(self):
        items = make_adapter()._parse(DATA, min_score=50)
        assert "efficient LLM inference" in items[0].title

    def test_external_url_preferred_for_link_posts(self):
        items = make_adapter()._parse(DATA, min_score=50)
        # first post is a link post → external URL
        assert items[0].url == "https://arxiv.org/abs/2603.00001"

    def test_self_post_uses_reddit_permalink(self):
        items = make_adapter()._parse(DATA, min_score=50)
        # second post is self post → reddit permalink
        assert "reddit.com" in items[1].url

    def test_excerpt_from_selftext(self):
        items = make_adapter()._parse(DATA, min_score=50)
        assert "experimenting" in items[1].excerpt

    def test_category_is_community(self):
        items = make_adapter()._parse(DATA, min_score=50)
        assert all(i.category == "community" for i in items)

    def test_published_at_from_created_utc(self):
        items = make_adapter()._parse(DATA, min_score=50)
        assert items[0].published_at is not None
        assert items[0].published_at.year in (2025, 2026)

    def test_score_in_metadata(self):
        items = make_adapter()._parse(DATA, min_score=50)
        assert items[0].raw_metadata["score"] == 500

    @pytest.mark.asyncio
    async def test_fetch_sets_user_agent(self):
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
        call_kwargs = cls.call_args.kwargs
        assert "User-Agent" in call_kwargs.get("headers", {})
