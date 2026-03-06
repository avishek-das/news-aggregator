import httpx
from app.adapters.base import RawItem, SourceAdapter
from app.adapters.rss_parser import parse_rss_feed

PWC_RSS_URL = "https://paperswithcode.com/latest.rss"


class PapersWithCodeAdapter(SourceAdapter):
    def _parse(self, xml_text: str) -> list[RawItem]:
        return parse_rss_feed(xml_text, category="research")

    async def fetch(self) -> list[RawItem]:
        url = self.fetch_config.get("url", PWC_RSS_URL)
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return self._parse(response.text)
