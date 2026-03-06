import xml.etree.ElementTree as ET
import httpx
from app.adapters.base import RawItem, SourceAdapter
from app.adapters.rss_parser import parse_rss_feed

ITUNES_NS = "http://www.itunes.com/dtds/podcast-1.0.dtd"


class PodcastsAdapter(SourceAdapter):
    def _parse(self, xml_text: str, podcast_name: str) -> list[RawItem]:
        base_items = parse_rss_feed(xml_text, category="media")
        # Enrich with duration from itunes:duration
        root = ET.fromstring(xml_text)
        durations: list[str] = []
        for item_el in root.findall("channel/item"):
            dur_el = item_el.find(f"{{{ITUNES_NS}}}duration")
            durations.append(dur_el.text.strip() if dur_el is not None and dur_el.text else "")

        enriched: list[RawItem] = []
        for i, item in enumerate(base_items):
            dur = durations[i] if i < len(durations) else ""
            enriched.append(RawItem(
                title=item.title,
                url=item.url,
                excerpt=item.excerpt,
                published_at=item.published_at,
                category=item.category,
                raw_metadata={"podcast_name": podcast_name, "duration": dur},
            ))
        return enriched

    async def fetch(self) -> list[RawItem]:
        feeds: list[dict] = self.fetch_config.get("feeds", [])
        all_items: list[RawItem] = []
        async with httpx.AsyncClient(timeout=30) as client:
            for feed in feeds:
                name = feed.get("name", "")
                url = feed.get("url", "")
                if not url:
                    continue
                response = await client.get(url)
                response.raise_for_status()
                all_items.extend(self._parse(response.text, name))
        return all_items
