from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from app.models.source import (
    SourceCreateRequest, SourceUpdateRequest,
    SourceResponse, SourceSingleResponse, SourcesListResponse,
)
import app.repositories.sources as repo

router = APIRouter(prefix="/sources", tags=["sources"])


def _to_response(source) -> SourceResponse:
    return SourceResponse(**source.model_dump())


@router.get("", response_model=SourcesListResponse)
def list_sources() -> SourcesListResponse:
    sources = repo.find_all()
    return SourcesListResponse(
        success=True,
        data=[_to_response(s) for s in sources],
    )


@router.post("", response_model=SourceSingleResponse, status_code=status.HTTP_201_CREATED)
def create_source(body: SourceCreateRequest) -> SourceSingleResponse:
    data = body.model_dump()
    source = repo.create(data)
    return SourceSingleResponse(success=True, data=_to_response(source))


@router.patch("/{source_id}", response_model=SourceSingleResponse)
def update_source(source_id: UUID, body: SourceUpdateRequest) -> SourceSingleResponse:
    data = {k: v for k, v in body.model_dump().items() if v is not None}
    source = repo.update(str(source_id), data)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return SourceSingleResponse(success=True, data=_to_response(source))


@router.post("/{source_id}/retire", response_model=SourceSingleResponse)
def retire_source(source_id: UUID) -> SourceSingleResponse:
    source = repo.update(str(source_id), {"status": "inactive"})
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return SourceSingleResponse(success=True, data=_to_response(source))


@router.post("/{source_id}/reactivate", response_model=SourceSingleResponse)
def reactivate_source(source_id: UUID) -> SourceSingleResponse:
    source = repo.update(str(source_id), {
        "status": "active",
        "consecutive_failures": 0,
        "last_error": None,
    })
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return SourceSingleResponse(success=True, data=_to_response(source))


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(source_id: UUID) -> None:
    existing = repo.find_by_id(str(source_id))
    if existing is None:
        raise HTTPException(status_code=404, detail="Source not found")
    if repo.has_items(str(source_id)):
        raise HTTPException(
            status_code=409,
            detail=f"Cannot delete source with existing items. Retire it instead.",
        )
    repo.delete(str(source_id))
