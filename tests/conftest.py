import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from redis.asyncio import Redis

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.core.redis import get_cache, RedisCache
from app.core.config import settings


# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/stock_assessor_test"


@pytest.fixture(scope="session")
def event_loop():
    """
    Create an event loop for the entire test session
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_engine():
    """
    Create a test database engine
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a test database session
    """
    async_session = async_sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session


@pytest.fixture(scope="function")
async def redis_client():
    """
    Create a test Redis client
    """
    client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=1,  # Use different DB for testing
        decode_responses=True,
    )

    await client.flushdb()

    yield client

    await client.flushdb()
    await client.close()


@pytest.fixture(scope="function")
async def test_cache(redis_client):
    """
    Create a test cache instance
    """
    cache = RedisCache()
    cache.redis = redis_client
    yield cache


@pytest.fixture(scope="function")
async def client(db_session, test_cache) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test HTTP client
    """
    async def override_get_db():
        yield db_session

    async def override_get_cache():
        return test_cache

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_cache] = override_get_cache

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
