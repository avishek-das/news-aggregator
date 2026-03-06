from fastapi import APIRouter
from app.config import settings

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        },
        "meta": None,
    }
