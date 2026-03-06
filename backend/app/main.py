from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, items
from app.middleware.session import SessionMiddleware

app = FastAPI(
    title="AI News Aggregator API",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
)

# CRITICAL: allow_credentials=True + explicit origins required for session cookies.
# Never use allow_origins=["*"] with allow_credentials=True.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SessionMiddleware must be added AFTER CORSMiddleware (Starlette processes in reverse order)
app.add_middleware(SessionMiddleware)

app.include_router(health.router)
app.include_router(items.router)
