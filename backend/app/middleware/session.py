import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.db.client import get_client

COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # 1 year


def _is_valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(value, version=4)
        return True
    except (ValueError, AttributeError):
        return False


def _upsert_session(session_id: str) -> None:
    try:
        get_client().table("user_sessions").upsert(
            {"session_id": session_id},
            on_conflict="session_id",
        ).execute()
    except Exception:
        pass  # never block a request over session tracking


def _touch_session(session_id: str) -> None:
    try:
        get_client().table("user_sessions").update(
            {"last_seen_at": "now()"}
        ).eq("session_id", session_id).execute()
    except Exception:
        pass


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: object) -> Response:
        existing = request.cookies.get("session_id")
        if existing and _is_valid_uuid(existing):
            session_id = existing
            _touch_session(session_id)
        else:
            session_id = str(uuid.uuid4())
            _upsert_session(session_id)

        request.state.session_id = session_id
        response: Response = await call_next(request)  # type: ignore[operator]
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            samesite="lax",
            max_age=COOKIE_MAX_AGE,
        )
        return response
