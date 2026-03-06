from app.adapters.base import SourceAdapter
from app.adapters.arxiv import ArxivAdapter
from app.adapters.arxiv_extra import ArxivExtraAdapter
from app.adapters.hackernews import HackerNewsAdapter
from app.adapters.papers_with_code import PapersWithCodeAdapter
from app.adapters.lobsters import LobstersAdapter
from app.adapters.lab_blogs import LabBlogsAdapter
from app.adapters.youtube import YouTubeAdapter
from app.adapters.podcasts import PodcastsAdapter
from app.adapters.reddit import RedditAdapter
from app.adapters.huggingface import HuggingFaceAdapter
from app.adapters.openreview import OpenReviewAdapter
from app.adapters.github_trending import GitHubTrendingAdapter

ADAPTER_REGISTRY: dict[str, type[SourceAdapter]] = {
    "arxiv": ArxivAdapter,
    "arxiv_extra": ArxivExtraAdapter,
    "hackernews": HackerNewsAdapter,
    "papers_with_code": PapersWithCodeAdapter,
    "lobsters": LobstersAdapter,
    "lab_blogs": LabBlogsAdapter,
    "youtube": YouTubeAdapter,
    "podcasts": PodcastsAdapter,
    "reddit": RedditAdapter,
    "huggingface": HuggingFaceAdapter,
    "openreview": OpenReviewAdapter,
    "github_trending": GitHubTrendingAdapter,
}


def get_adapter(name: str, source_id: str, fetch_config: dict) -> SourceAdapter:
    cls = ADAPTER_REGISTRY.get(name)
    if cls is None:
        raise ValueError(f"Unknown adapter: '{name}'. Available: {list(ADAPTER_REGISTRY)}")
    return cls(source_id=source_id, fetch_config=fetch_config)
