from app.adapters.base import SourceAdapter
from app.adapters.arxiv import ArxivAdapter
from app.adapters.hackernews import HackerNewsAdapter

ADAPTER_REGISTRY: dict[str, type[SourceAdapter]] = {
    "arxiv": ArxivAdapter,
    "hackernews": HackerNewsAdapter,
}


def get_adapter(name: str, source_id: str, fetch_config: dict) -> SourceAdapter:
    cls = ADAPTER_REGISTRY.get(name)
    if cls is None:
        raise ValueError(f"Unknown adapter: '{name}'. Available: {list(ADAPTER_REGISTRY)}")
    return cls(source_id=source_id, fetch_config=fetch_config)
