from datetime import datetime
from typing import Literal, Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

SourceType = Literal["rss", "api", "scrape"]
SourceCategory = Literal["research", "code", "community", "product", "media"]
SourcePriority = Literal["high", "medium", "low"]
SourceStatus = Literal["active", "inactive", "flagged"]

VALID_ADAPTERS = {
    "arxiv", "arxiv_extra", "hackernews", "papers_with_code", "lobsters",
    "lab_blogs", "youtube", "podcasts", "reddit", "huggingface",
    "openreview", "github_trending",
}


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
    updated_at: datetime | None = None
    created_at: datetime | None = None


class SourceResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    name: str
    url: str
    type: SourceType
    category: SourceCategory
    priority: SourcePriority
    status: SourceStatus
    fetch_config: dict
    last_fetched_at: datetime | None = None
    last_error: str | None = None
    consecutive_failures: int = 0
    updated_at: datetime | None = None
    created_at: datetime | None = None


class SourcesListResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    success: bool
    data: list[SourceResponse]
    error: str | None = None


class SourceSingleResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    success: bool
    data: SourceResponse | None
    error: str | None = None


class SourceCreateRequest(BaseModel):
    name: str
    url: str
    type: SourceType
    category: SourceCategory
    priority: SourcePriority
    fetch_config: dict = {}

    @field_validator("fetch_config")
    @classmethod
    def validate_adapter(cls, v: dict) -> dict:
        adapter = v.get("adapter")
        if adapter and adapter not in VALID_ADAPTERS:
            raise ValueError(f"Unknown adapter '{adapter}'. Valid: {sorted(VALID_ADAPTERS)}")
        return v


class SourceUpdateRequest(BaseModel):
    name: str | None = None
    url: str | None = None
    type: SourceType | None = None
    category: SourceCategory | None = None
    priority: SourcePriority | None = None
    status: SourceStatus | None = None
    fetch_config: dict | None = None

    @field_validator("fetch_config")
    @classmethod
    def validate_adapter(cls, v: dict | None) -> dict | None:
        if v is not None:
            adapter = v.get("adapter")
            if adapter and adapter not in VALID_ADAPTERS:
                raise ValueError(f"Unknown adapter '{adapter}'. Valid: {sorted(VALID_ADAPTERS)}")
        return v

    @model_validator(mode="after")
    def at_least_one_field(self) -> "SourceUpdateRequest":
        values = {k: v for k, v in self.__dict__.items() if v is not None}
        if not values:
            raise ValueError("At least one field must be provided for update")
        return self
