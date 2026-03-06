from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class Source(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    name: str
    url: str
    type: str
    category: str
    priority: str
    status: str
    fetch_config: dict
    last_fetched_at: datetime | None = None
    last_error: str | None = None
    consecutive_failures: int = 0
    created_at: datetime | None = None
