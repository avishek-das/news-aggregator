from datetime import datetime
import httpx
from app.adapters.base import RawItem, SourceAdapter

HF_DAILY_PAPERS = "https://huggingface.co/api/daily_papers"
HF_PAPER_URL = "https://huggingface.co/papers/{paper_id}"


class HuggingFaceAdapter(SourceAdapter):
    def _parse(self, data: list[dict]) -> list[RawItem]:
        items: list[RawItem] = []
        for entry in data:
            title = (entry.get("title") or "").strip()
            paper = entry.get("paper") or {}
            paper_id = paper.get("id", "")
            url = HF_PAPER_URL.format(paper_id=paper_id) if paper_id else ""
            summary = (paper.get("summary") or "").strip()[:500]
            authors = [a.get("name", "") for a in paper.get("authors", [])]
            published_str = entry.get("publishedAt")
            pub: datetime | None = None
            if published_str:
                try:
                    pub = datetime.fromisoformat(
                        published_str.replace("Z", "+00:00")
                    )
                except ValueError:
                    pass

            if title and url:
                items.append(RawItem(
                    title=title,
                    url=url,
                    excerpt=summary,
                    published_at=pub,
                    category="research",
                    raw_metadata={"authors": authors},
                ))
        return items

    async def fetch(self) -> list[RawItem]:
        url = self.fetch_config.get("url", HF_DAILY_PAPERS)
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url)
            response.raise_for_status()
            return self._parse(response.json())
