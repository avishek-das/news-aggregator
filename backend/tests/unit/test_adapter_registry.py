"""TDD: Adapter registry tests."""
import pytest
from app.adapters import get_adapter
from app.adapters.arxiv import ArxivAdapter
from app.adapters.hackernews import HackerNewsAdapter


def test_get_adapter_arxiv() -> None:
    adapter = get_adapter("arxiv", "src-id", {"url": "https://example.com"})
    assert isinstance(adapter, ArxivAdapter)


def test_get_adapter_hackernews() -> None:
    adapter = get_adapter("hackernews", "src-id", {})
    assert isinstance(adapter, HackerNewsAdapter)


def test_get_adapter_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unknown adapter"):
        get_adapter("unknown_adapter", "src-id", {})
