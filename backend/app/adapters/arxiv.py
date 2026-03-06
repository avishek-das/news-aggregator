import xml.etree.ElementTree as ET
import httpx
from datetime import datetime, timezone
from app.adapters.base import RawItem, SourceAdapter

ATOM_NS = "http://www.w3.org/2005/Atom"


class ArxivAdapter(SourceAdapter):
    def __init__(self, source_id: str, fetch_config: dict, url: str | None = None) -> None:
        super().__init__(source_id, fetch_config)
        self._url = url or fetch_config.get("url", "")

    def _parse(self, xml_text: str) -> list[RawItem]:
        root = ET.fromstring(xml_text)
        items: list[RawItem] = []
        for entry in root.findall(f"{{{ATOM_NS}}}entry"):
            title_el = entry.find(f"{{{ATOM_NS}}}title")
            id_el = entry.find(f"{{{ATOM_NS}}}id")
            summary_el = entry.find(f"{{{ATOM_NS}}}summary")
            published_el = entry.find(f"{{{ATOM_NS}}}published")
            authors = [
                a.findtext(f"{{{ATOM_NS}}}name", "")
                for a in entry.findall(f"{{{ATOM_NS}}}author")
            ]
            title = " ".join((title_el.text or "").split()) if title_el is not None else ""
            url = (id_el.text or "").strip() if id_el is not None else ""
            excerpt = " ".join((summary_el.text or "").split())[:500] if summary_el is not None else ""
            published_at: datetime | None = None
            if published_el is not None and published_el.text:
                try:
                    published_at = datetime.fromisoformat(published_el.text.replace("Z", "+00:00"))
                except ValueError:
                    pass
            items.append(RawItem(
                title=title,
                url=url,
                excerpt=excerpt,
                published_at=published_at,
                category="research",
                raw_metadata={"authors": authors},
            ))
        return items

    async def fetch(self) -> list[RawItem]:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(self._url)
            response.raise_for_status()
            return self._parse(response.text)
