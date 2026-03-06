"""TDD: Session middleware tests."""
from unittest.mock import patch, MagicMock
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient


def make_app_with_session() -> FastAPI:
    with patch("app.middleware.session.get_client", return_value=MagicMock()):
        from app.middleware.session import SessionMiddleware
        app = FastAPI()
        app.add_middleware(SessionMiddleware)

        @app.get("/test")
        async def test_route(request: Request) -> dict:
            return {"session_id": request.state.session_id}

        return app


def test_no_cookie_generates_session_id() -> None:
    with patch("app.middleware.session.get_client", return_value=MagicMock()):
        app = make_app_with_session()
        client = TestClient(app)
        resp = client.get("/test")
        assert resp.status_code == 200
        data = resp.json()
        assert "session_id" in data
        assert len(data["session_id"]) == 36
        assert "session_id" in resp.cookies


def test_existing_valid_cookie_is_reused() -> None:
    import uuid
    with patch("app.middleware.session.get_client", return_value=MagicMock()):
        app = make_app_with_session()
        client = TestClient(app)
        existing = str(uuid.uuid4())
        client.cookies.set("session_id", existing)
        resp = client.get("/test")
        assert resp.json()["session_id"] == existing


def test_invalid_uuid_cookie_is_replaced() -> None:
    with patch("app.middleware.session.get_client", return_value=MagicMock()):
        app = make_app_with_session()
        client = TestClient(app)
        client.cookies.set("session_id", "not-a-uuid")
        resp = client.get("/test")
        new_id = resp.json()["session_id"]
        assert new_id != "not-a-uuid"
        assert len(new_id) == 36


def test_cookie_is_httponly() -> None:
    with patch("app.middleware.session.get_client", return_value=MagicMock()):
        app = make_app_with_session()
        client = TestClient(app)
        resp = client.get("/test")
        set_cookie = resp.headers.get("set-cookie", "")
        assert "httponly" in set_cookie.lower()
