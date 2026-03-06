import xml.etree.ElementTree as ET
import httpx
from datetime import datetime
from app.adapters.base import RawItem, SourceAdapter

ATOM_NS = "http://www.w3.org/2005/Atom"
YT_NS = "http://www.youtube.com/xml/schemas/2015"
MEDIA_NS = "http://search.yahoo.com/mrss/"
YT_FEED = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


class YouTubeAdapter(SourceAdapter):
    def _parse(self, xml_text: str, channel_name: str) -> list[RawItem]:
        root = ET.fromstring(xml_text)
        items: list[RawItem] = []
        for entry in root.findall(f"{{{ATOM_NS}}}entry"):
            title_el = entry.find(f"{{{ATOM_NS}}}title")
            link_el = entry.find(f"{{{ATOM_NS}}}link[@rel='alternate']")
            pub_el = entry.find(f"{{{ATOM_NS}}}published")
            video_id_el = entry.find(f"{{{YT_NS}}}videoId")
            media_group = entry.find(f"{{{MEDIA_NS}}}group")
            desc_el = (
                media_group.find(f"{{{MEDIA_NS}}}description")
                if media_group is not None
                else None
            )

            title = (title_el.text or "").strip() if title_el is not None else ""
            url = link_el.get("href", "") if link_el is not None else ""
            video_id = video_id_el.text if video_id_el is not None else ""
            excerpt = (desc_el.text or "").strip()[:500] if desc_el is not None else ""
            pub: datetime | None = None
            if pub_el is not None and pub_el.text:
                try:
                    pub = datetime.fromisoformat(pub_el.text.replace("Z", "+00:00"))
                except ValueError:
                    pass

            if title and url:
                items.append(RawItem(
                    title=title,
                    url=url,
                    excerpt=excerpt,
                    published_at=pub,
                    category="media",
                    raw_metadata={"channel_name": channel_name, "video_id": video_id},
                ))
        return items

    async def fetch(self) -> list[RawItem]:
        channels: list[dict] = self.fetch_config.get("channels", [])
        all_items: list[RawItem] = []
        async with httpx.AsyncClient(timeout=30) as client:
            for ch in channels:
                cid = ch.get("channel_id", "")
                name = ch.get("name", "")
                if not cid:
                    continue
                url = YT_FEED.format(channel_id=cid)
                response = await client.get(url)
                response.raise_for_status()
                all_items.extend(self._parse(response.text, name))
        return all_items
