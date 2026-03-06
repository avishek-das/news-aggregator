import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
from app.adapters.github_trending import GitHubTrendingAdapter

FIXTURES = Path(__file__).parent.parent / "fixtures"
HTML = (FIXTURES / "github_trending.html").read_text()


def make_adapter(language="python"):
    return GitHubTrendingAdapter(
        source_id="test",
        fetch_config={"language": language},
    )


class TestGitHubTrendingAdapter:
    def test_parse_returns_correct_count(self):
        items = make_adapter()._parse(HTML, "python")
        assert len(items) == 2

    def test_repo_url_correct(self):
        items = make_adapter()._parse(HTML, "python")
        assert items[0].url == "https://github.com/huggingface/transformers"

    def test_title_is_owner_slash_repo(self):
        items = make_adapter()._parse(HTML, "python")
        assert items[0].title == "huggingface/transformers"

    def test_description_as_excerpt(self):
        items = make_adapter()._parse(HTML, "python")
        assert "Machine Learning" in items[0].excerpt

    def test_category_is_code(self):
        items = make_adapter()._parse(HTML, "python")
        assert all(i.category == "code" for i in items)

    def test_language_in_metadata(self):
        items = make_adapter()._parse(HTML, "python")
        assert all(i.raw_metadata["language"] == "python" for i in items)

    def test_parse_returns_empty_on_garbage_html(self):
        items = make_adapter()._parse("<html><body>nothing here</body></html>", "python")
        assert items == []

    @pytest.mark.asyncio
    async def test_fetch_builds_url_with_language(self):
        adapter = make_adapter("jupyter-notebook")
        mock_response = MagicMock(raise_for_status=MagicMock(), text=HTML)
        with patch("httpx.AsyncClient") as cls:
            mc = AsyncMock()
            mc.__aenter__ = AsyncMock(return_value=mc)
            mc.__aexit__ = AsyncMock(return_value=None)
            mc.get = AsyncMock(return_value=mock_response)
            cls.return_value = mc
            await adapter.fetch()
        url_called = mc.get.call_args.args[0]
        assert "jupyter-notebook" in url_called
