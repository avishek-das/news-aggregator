"""TDD: config.py validation tests written before implementation."""
import os
from unittest.mock import patch

import pytest
from pydantic import ValidationError


def test_config_loads_with_all_required_vars() -> None:
    env = {
        "DATABASE_URL": "postgresql://postgres:pass@localhost:5432/news_aggregator",
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_ANON_KEY": "test-anon-key",
        "SUPABASE_SERVICE_KEY": "test-service-key",
    }
    with patch.dict(os.environ, env, clear=True):
        from importlib import import_module, reload
        import app.config as config_module
        reload(config_module)
        settings = config_module.Settings()
        assert settings.DATABASE_URL == env["DATABASE_URL"]
        assert settings.SUPABASE_URL == env["SUPABASE_URL"]


def test_config_missing_database_url_raises() -> None:
    env = {
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_ANON_KEY": "test-anon-key",
        "SUPABASE_SERVICE_KEY": "test-service-key",
    }
    with patch.dict(os.environ, env, clear=True):
        from app.config import Settings
        from pydantic_settings import SettingsConfigDict
        # Override env_file to prevent .env file from satisfying missing vars
        class SettingsNoFile(Settings):
            model_config = SettingsConfigDict(env_file=None, extra="ignore")
        with pytest.raises(ValidationError) as exc_info:
            SettingsNoFile()
        assert "DATABASE_URL" in str(exc_info.value)


def test_config_optional_fields_have_defaults() -> None:
    env = {
        "DATABASE_URL": "postgresql://postgres:pass@localhost:5432/db",
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_ANON_KEY": "key",
        "SUPABASE_SERVICE_KEY": "key",
    }
    with patch.dict(os.environ, env, clear=True):
        from app.config import Settings
        s = Settings()
        assert s.LLM_MODEL == "gemini/gemini-1.5-flash"
        assert s.DAILY_LLM_COST_CAP_USD == 0.0
        assert s.ENVIRONMENT == "development"
