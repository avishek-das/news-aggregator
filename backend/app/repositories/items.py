from datetime import datetime
from uuid import UUID
from app.adapters.base import RawItem
from app.db.client import get_client
from app.models.item import ItemResponse, Meta


def upsert(items: list[RawItem], source_id: str) -> int:
    if not items:
        return 0
    rows = [
        {
            "source_id": source_id,
            "title": item.title,
            "url": item.url,
            "excerpt": item.excerpt[:1000] if item.excerpt else None,
            "published_at": item.published_at.isoformat() if item.published_at else None,
            "category": item.category,
            "is_paywalled": item.is_paywalled,
            "raw_metadata": item.raw_metadata,
        }
        for item in items
    ]
    result = get_client().table("items").upsert(
        rows, on_conflict="url", ignore_duplicates=True
    ).execute()
    return len(result.data) if result.data else 0


def find_all(
    *,
    category: str | None = None,
    source_id: str | None = None,
    limit: int = 10,
    offset: int = 0,
    session_id: str | None = None,
) -> tuple[list[ItemResponse], int]:
    limit = min(limit, 100)
    client = get_client()

    query = client.table("items").select("*, sources(name)", count="exact").order(
        "published_at", desc=True
    )
    if category:
        query = query.eq("category", category)
    if source_id:
        query = query.eq("source_id", source_id)

    result = query.range(offset, offset + limit - 1).execute()
    rows = result.data or []
    total = result.count or 0

    # Fetch read state for this session
    read_ids: set[str] = set()
    if session_id and rows:
        item_ids = [r["id"] for r in rows]
        read_result = client.table("read_items").select("item_id").eq(
            "session_id", session_id
        ).in_("item_id", item_ids).execute()
        read_ids = {r["item_id"] for r in (read_result.data or [])}

    items = [
        ItemResponse(
            id=UUID(row["id"]),
            source_id=UUID(row["source_id"]),
            source_name=(row.get("sources") or {}).get("name", ""),
            title=row["title"],
            url=row["url"],
            excerpt=row.get("excerpt"),
            summary=row.get("summary"),
            published_at=_parse_dt(row.get("published_at")),
            category=row["category"],
            is_paywalled=row.get("is_paywalled", False),
            is_read=row["id"] in read_ids,
            created_at=_parse_dt(row["created_at"]) or datetime.min,
        )
        for row in rows
    ]
    return items, total


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None
