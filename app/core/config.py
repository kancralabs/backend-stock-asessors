from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings and configuration
    """

    # API Settings
    PROJECT_NAME: str = "Stock Assessor API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/stock_assessor"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    REDIS_CACHE_TTL: int = 3600  # 1 hour default

    # Alpha Vantage
    ALPHA_VANTAGE_API_KEY: str = ""
    ALPHA_VANTAGE_BASE_URL: str = "https://www.alphavantage.co/query"

    # GDELT
    GDELT_BASE_URL: str = "https://api.gdeltproject.org/api/v2"

    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    ALPHA_VANTAGE_RATE_LIMIT: int = 5  # calls per minute for free tier

    # Scheduler
    SCHEDULER_TIMEZONE: str = "Asia/Jakarta"
    DATA_FETCH_CRON: str = "0 */4 * * *"  # Every 4 hours

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Cache settings to avoid reading .env multiple times
    """
    return Settings()


settings = get_settings()
