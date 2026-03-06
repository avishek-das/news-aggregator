"""TDD: Supabase client singleton tests."""
from unittest.mock import MagicMock, patch


def test_get_client_returns_supabase_client() -> None:
    mock_client = MagicMock()
    with patch("app.db.client.create_client", return_value=mock_client):
        import importlib
        import app.db.client as mod
        mod._client = None  # reset singleton
        importlib.reload(mod)
        from app.db.client import get_client
        result = get_client()
        assert result is not None


def test_get_client_is_singleton() -> None:
    mock_client = MagicMock()
    with patch("app.db.client.create_client", return_value=mock_client):
        import app.db.client as mod
        mod._client = None
        from app.db.client import get_client
        c1 = get_client()
        c2 = get_client()
        assert c1 is c2
