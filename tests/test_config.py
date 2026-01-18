import pytest
from app.core.config import Settings, get_settings


def test_settings_creation():
    """
    Test settings creation
    """
    settings = Settings()
    assert settings.PROJECT_NAME == "Stock Assessor API"
    assert settings.VERSION == "1.0.0"
    assert settings.API_V1_STR == "/api/v1"


def test_get_settings():
    """
    Test get_settings function returns cached settings
    """
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2  # Should be the same instance (cached)


def test_settings_default_values():
    """
    Test default values in settings
    """
    settings = Settings()
    assert settings.REDIS_PORT == 6379
    assert settings.REDIS_DB == 0
    assert settings.REDIS_CACHE_TTL == 3600
    assert settings.RATE_LIMIT_PER_MINUTE == 60
    assert settings.ALPHA_VANTAGE_RATE_LIMIT == 5


def test_settings_allowed_origins():
    """
    Test CORS allowed origins
    """
    settings = Settings()
    assert isinstance(settings.ALLOWED_ORIGINS, list)
    assert len(settings.ALLOWED_ORIGINS) > 0
