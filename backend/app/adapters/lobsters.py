import httpx
from app.adapters.base import RawItem, SourceAdapter
from app.adapters.rss_parser import parse_rss_feed


class LobstersAdapter(SourceAdapter):
    def _parse(self, xml_text: str) -> list[RawItem]:
        return parse_rss_feed(xml_text, category="community")

    async def fetch(self) -> list[RawItem]:
        tags: list[str] = self.fetch_config.get("tags", ["ai"])
        all_items: list[RawItem] = []
        seen_urls: set[str] = set()
        async with httpx.AsyncClient(timeout=30) as client:
            for tag in tags:
                url = f"https://lobste.rs/t/{tag}.rss"
                try:
                    response = await client.get(url)
                    response.raise_for_status()
                    for item in self._parse(response.text):
                        if item.url not in seen_urls:
                            seen_urls.add(item.url)
                            all_items.append(item)
                except Exception:
                    continue
        return all_items
