import httpx
from app.adapters.arxiv import ArxivAdapter
from app.adapters.base import RawItem

ARXIV_BASE = "https://export.arxiv.org/api/query"


class ArxivExtraAdapter(ArxivAdapter):
    """Fetches multiple arXiv categories (cs.LG, cs.CL, cs.CV, stat.ML)."""

    def __init__(self, source_id: str, fetch_config: dict) -> None:
        super().__init__(source_id, fetch_config)
        self._categories: list[str] = fetch_config.get("categories", ["cs.LG"])
        self._max_results: int = fetch_config.get("max_results", 30)

    async def fetch(self) -> list[RawItem]:
        all_items: list[RawItem] = []
        seen_urls: set[str] = set()
        async with httpx.AsyncClient(timeout=30) as client:
            for cat in self._categories:
                url = (
                    f"{ARXIV_BASE}?search_query=cat:{cat}"
                    f"&sortBy=submittedDate&max_results={self._max_results}"
                )
                response = await client.get(url)
                response.raise_for_status()
                for item in self._parse(response.text):
                    if item.url not in seen_urls:
                        seen_urls.add(item.url)
                        all_items.append(item)
        return all_items
