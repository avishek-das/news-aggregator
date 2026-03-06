from uuid import UUID
from fastapi import APIRouter, Query, Request, Response
from app.db.client import get_client
from app.models.item import ItemsListResponse, Meta
from app.repositories.items import find_all

router = APIRouter()

VALID_CATEGORIES = {"research", "code", "community", "product", "media"}


@router.get("/items", response_model=ItemsListResponse)
async def list_items(
    request: Request,
    category: str | None = None,
    source_id: str | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> ItemsListResponse:
    if category and category not in VALID_CATEGORIES:
        return ItemsListResponse(
            success=False, data=[], error=f"Invalid category: '{category}'",
            meta=Meta(total=0, limit=limit, offset=offset),
        )
    session_id: str | None = getattr(request.state, "session_id", None)
    items, total = find_all(
        category=category,
        source_id=source_id,
        limit=limit,
        offset=offset,
        session_id=session_id,
    )
    return ItemsListResponse(
        success=True, data=items, error=None,
        meta=Meta(total=total, limit=limit, offset=offset),
    )


@router.post("/items/{item_id}/read", status_code=204)
async def mark_read(item_id: UUID, request: Request) -> Response:
    session_id: str = getattr(request.state, "session_id", "anonymous")
    get_client().table("read_items").upsert(
        {"session_id": session_id, "item_id": str(item_id)},
        on_conflict="session_id,item_id",
    ).execute()
    return Response(status_code=204)
