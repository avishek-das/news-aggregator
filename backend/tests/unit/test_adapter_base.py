"""TDD: SourceAdapter ABC and RawItem dataclass tests."""
import pytest
from datetime import datetime, timezone
from app.adapters.base import RawItem, SourceAdapter


def test_raw_item_creation() -> None:
    item = RawItem(
        title="Test",
        url="https://example.com",
        excerpt="Short summary",
        published_at=datetime.now(timezone.utc),
        category="research",
    )
    assert item.title == "Test"
    assert item.is_paywalled is False
    assert item.raw_metadata == {}


def test_raw_item_is_frozen() -> None:
    item = RawItem(title="T", url="u", excerpt="e", published_at=None, category="research")
    with pytest.raises((TypeError, AttributeError)):
        item.title = "changed"  # type: ignore


def test_source_adapter_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        SourceAdapter(source_id="abc", fetch_config={})  # type: ignore


def test_concrete_adapter_must_implement_fetch() -> None:
    class BadAdapter(SourceAdapter):
        pass
    with pytest.raises(TypeError):
        BadAdapter(source_id="abc", fetch_config={})  # type: ignore


def test_concrete_adapter_with_fetch_works() -> None:
    class GoodAdapter(SourceAdapter):
        async def fetch(self) -> list[RawItem]:
            return []
    adapter = GoodAdapter(source_id="abc", fetch_config={})
    assert adapter.source_id == "abc"
