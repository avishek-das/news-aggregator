from datetime import datetime, timezone
from app.db.client import get_client
from app.models.source import Source


def find_active() -> list[Source]:
    data = get_client().table("sources").select("*").eq("status", "active").execute().data
    return [Source(**row) for row in data]


def record_success(source_id: str, item_count: int) -> None:
    get_client().table("sources").update({
        "last_fetched_at": datetime.now(timezone.utc).isoformat(),
        "consecutive_failures": 0,
        "last_error": None,
    }).eq("id", source_id).execute()


def record_failure(source_id: str, error: str) -> None:
    row = get_client().table("sources").select("consecutive_failures").eq("id", source_id).single().execute().data
    new_failures = (row.get("consecutive_failures") or 0) + 1
    update: dict = {
        "consecutive_failures": new_failures,
        "last_error": error,
        "last_fetched_at": datetime.now(timezone.utc).isoformat(),
    }
    if new_failures >= 3:
        update["status"] = "flagged"
    get_client().table("sources").update(update).eq("id", source_id).execute()
