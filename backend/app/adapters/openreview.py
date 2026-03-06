import httpx
from app.adapters.base import RawItem, SourceAdapter

OPENREVIEW_API = "https://api2.openreview.net/notes"
OPENREVIEW_URL = "https://openreview.net/forum?id={note_id}"


class OpenReviewAdapter(SourceAdapter):
    def _parse(self, data: dict) -> list[RawItem]:
        items: list[RawItem] = []
        for note in data.get("notes", []):
            note_id = note.get("id", "")
            content = note.get("content", {})
            title = (content.get("title", {}).get("value") or "").strip()
            abstract = (content.get("abstract", {}).get("value") or "").strip()[:500]
            authors = content.get("authors", {}).get("value", [])
            url = OPENREVIEW_URL.format(note_id=note_id) if note_id else ""

            if title and url:
                items.append(RawItem(
                    title=title,
                    url=url,
                    excerpt=abstract,
                    published_at=None,
                    category="research",
                    raw_metadata={"authors": authors},
                ))
        return items

    async def fetch(self) -> list[RawItem]:
        venues: list[str] = self.fetch_config.get("venues", [])
        all_items: list[RawItem] = []
        async with httpx.AsyncClient(timeout=30) as client:
            for venue in venues:
                params = {"content.venue": venue, "limit": 50, "offset": 0}
                response = await client.get(OPENREVIEW_API, params=params)
                response.raise_for_status()
                all_items.extend(self._parse(response.json()))
        return all_items
