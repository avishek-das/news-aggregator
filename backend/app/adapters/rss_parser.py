"""Shared RSS 2.0 / Atom feed parser. Returns list[RawItem]."""
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from app.adapters.base import RawItem

ATOM_NS = "http://www.w3.org/2005/Atom"


def _parse_date(text: str | None) -> datetime | None:
    if not text:
        return None
    text = text.strip()
    # ISO 8601 (Atom)
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        pass
    # RFC 2822 (RSS 2.0)
    try:
        return parsedate_to_datetime(text).astimezone(timezone.utc)
    except Exception:
        return None


def _truncate(text: str, limit: int = 500) -> str:
    return text[:limit] if len(text) > limit else text


def _parse_rss2(root: ET.Element, category: str) -> list[RawItem]:
    items: list[RawItem] = []
    for item in root.findall("channel/item"):
        title = (item.findtext("title") or "").strip()
        url = (item.findtext("link") or "").strip()
        desc = (item.findtext("description") or "").strip()
        pub = _parse_date(item.findtext("pubDate"))
        if title and url:
            items.append(RawItem(
                title=title,
                url=url,
                excerpt=_truncate(desc),
                published_at=pub,
                category=category,
            ))
    return items


def _parse_atom(root: ET.Element, category: str) -> list[RawItem]:
    items: list[RawItem] = []
    for entry in root.findall(f"{{{ATOM_NS}}}entry"):
        title_el = entry.find(f"{{{ATOM_NS}}}title")
        link_el = entry.find(f"{{{ATOM_NS}}}link[@rel='alternate']")
        if link_el is None:
            link_el = entry.find(f"{{{ATOM_NS}}}link")
        id_el = entry.find(f"{{{ATOM_NS}}}id")
        summary_el = entry.find(f"{{{ATOM_NS}}}summary")
        pub_el = entry.find(f"{{{ATOM_NS}}}published")

        title = (title_el.text or "").strip() if title_el is not None else ""
        url = ""
        if link_el is not None:
            url = link_el.get("href", "") or (link_el.text or "")
        if not url and id_el is not None:
            url = (id_el.text or "").strip()
        excerpt = (summary_el.text or "").strip() if summary_el is not None else ""
        pub = _parse_date(pub_el.text if pub_el is not None else None)

        if title and url:
            items.append(RawItem(
                title=title,
                url=url,
                excerpt=_truncate(excerpt),
                published_at=pub,
                category=category,
            ))
    return items


def parse_rss_feed(xml_text: str, category: str) -> list[RawItem]:
    """Parse RSS 2.0 or Atom XML and return list[RawItem] with given category."""
    root = ET.fromstring(xml_text)
    tag = root.tag
    if tag == "rss" or tag == "channel":
        return _parse_rss2(root, category)
    if tag == f"{{{ATOM_NS}}}feed" or tag == "feed":
        return _parse_atom(root, category)
    # Fallback: try RSS then Atom
    rss_items = _parse_rss2(root, category)
    return rss_items if rss_items else _parse_atom(root, category)
