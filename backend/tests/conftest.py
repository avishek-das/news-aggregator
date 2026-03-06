import os
import pytest
from fastapi.testclient import TestClient

# Set required env vars before any app module is imported
os.environ.setdefault("DATABASE_URL", "postgresql://postgres:test@localhost:5432/test")
os.environ.setdefault("SUPABASE_URL", "https://test.supabase.co")
os.environ.setdefault("SUPABASE_ANON_KEY", "test-anon-key")
os.environ.setdefault("SUPABASE_SERVICE_KEY", "test-service-key")


@pytest.fixture
def client() -> TestClient:
    from app.main import app
    return TestClient(app)
