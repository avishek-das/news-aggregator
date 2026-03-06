import httpx
from datetime import datetime
from app.adapters.base import RawItem, SourceAdapter

HN_BASE = "https://hn.algolia.com/api/v1/search"


class HackerNewsAdapter(SourceAdapter):
    def _parse(self, hits: list[dict]) -> list[RawItem]:
        min_score = self.fetch_config.get("min_score", 10)
        items: list[RawItem] = []
        for hit in hits:
            if (hit.get("points") or 0) < min_score:
                continue
            url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}"
            excerpt = (hit.get("story_text") or "")[:500]
            published_at: datetime | None = None
            if hit.get("created_at"):
                try:
                    published_at = datetime.fromisoformat(
                        hit["created_at"].replace("Z", "+00:00")
                    )
                except ValueError:
                    pass
            items.append(RawItem(
                title=hit.get("title", ""),
                url=url,
                excerpt=excerpt,
                published_at=published_at,
                category="community",
                raw_metadata={
                    "score": hit.get("points"),
                    "num_comments": hit.get("num_comments"),
                    "objectID": hit.get("objectID"),
                },
            ))
        return items

    async def fetch(self) -> list[RawItem]:
        url = self.fetch_config.get("url", HN_BASE)
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return self._parse(data.get("hits", []))
