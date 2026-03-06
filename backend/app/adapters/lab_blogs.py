import logging
import httpx
from app.adapters.base import RawItem, SourceAdapter
from app.adapters.rss_parser import parse_rss_feed

logger = logging.getLogger(__name__)


class LabBlogsAdapter(SourceAdapter):
    def _parse(self, xml_text: str, lab_name: str) -> list[RawItem]:
        items = parse_rss_feed(xml_text, category="research")
        return [
            RawItem(
                title=i.title,
                url=i.url,
                excerpt=i.excerpt,
                published_at=i.published_at,
                category=i.category,
                raw_metadata={"lab": lab_name},
            )
            for i in items
        ]

    async def fetch(self) -> list[RawItem]:
        feeds: list[dict] = self.fetch_config.get("feeds", [])
        all_items: list[RawItem] = []
        async with httpx.AsyncClient(timeout=30) as client:
            for feed in feeds:
                name = feed.get("name", "")
                url = feed.get("url", "")
                if not url:
                    continue
                try:
                    response = await client.get(url, follow_redirects=True)
                    response.raise_for_status()
                    all_items.extend(self._parse(response.text, name))
                except Exception as exc:
                    logger.warning("Lab blog feed '%s' failed: %s", name, exc)
        return all_items
