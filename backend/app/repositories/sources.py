from datetime import datetime, timezone
from app.db.client import get_client
from app.models.source import Source


def find_all() -> list[Source]:
    data = get_client().table("sources").select("*").order("name").execute().data
    return [Source(**row) for row in data]


def find_active() -> list[Source]:
    data = get_client().table("sources").select("*").eq("status", "active").execute().data
    return [Source(**row) for row in data]


def find_by_id(source_id: str) -> Source | None:
    result = get_client().table("sources").select("*").eq("id", source_id).execute().data
    if not result:
        return None
    return Source(**result[0])


def create(data: dict) -> Source:
    result = get_client().table("sources").insert(data).execute().data
    return Source(**result[0])


def update(source_id: str, data: dict) -> Source | None:
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    result = (
        get_client().table("sources")
        .update(data)
        .eq("id", source_id)
        .execute()
        .data
    )
    if not result:
        return None
    return Source(**result[0])


def delete(source_id: str) -> None:
    get_client().table("sources").delete().eq("id", source_id).execute()


def has_items(source_id: str) -> bool:
    result = (
        get_client().table("items")
        .select("id", count="exact")
        .eq("source_id", source_id)
        .limit(1)
        .execute()
    )
    return (result.count or 0) > 0


def record_success(source_id: str, item_count: int) -> None:
    get_client().table("sources").update({
        "last_fetched_at": datetime.now(timezone.utc).isoformat(),
        "consecutive_failures": 0,
        "last_error": None,
    }).eq("id", source_id).execute()


def record_failure(source_id: str, error: str) -> None:
    row = get_client().table("sources").select("consecutive_failures").eq("id", source_id).single().execute().data
    new_failures = (row.get("consecutive_failures") or 0) + 1
    update_data: dict = {
        "consecutive_failures": new_failures,
        "last_error": error,
        "last_fetched_at": datetime.now(timezone.utc).isoformat(),
    }
    if new_failures >= 3:
        update_data["status"] = "flagged"
    get_client().table("sources").update(update_data).eq("id", source_id).execute()
