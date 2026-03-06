from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Required
    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str

    # CORS — comma-separated list of allowed origins
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # LLM — switch model via env var, no code changes needed
    LLM_MODEL: str = "gemini/gemini-1.5-flash"
    LLM_HIGH_SIGNAL_MODEL: str = "gemini/gemini-1.5-flash"
    DAILY_LLM_COST_CAP_USD: float = 0.0

    # App
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    APP_VERSION: str = "0.1.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Fail fast at import time if required vars are missing.
# In ECS, all vars are injected from Secrets Manager by the task definition.
settings = Settings()
