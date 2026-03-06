from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class ItemResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    source_id: UUID
    source_name: str
    title: str
    url: str
    excerpt: str | None = None
    summary: str | None = None
    published_at: datetime | None = None
    category: str
    is_paywalled: bool = False
    is_read: bool = False
    created_at: datetime


class Meta(BaseModel):
    model_config = ConfigDict(frozen=True)

    total: int
    limit: int
    offset: int


class ItemsListResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    success: bool
    data: list[ItemResponse]
    error: str | None
    meta: Meta
