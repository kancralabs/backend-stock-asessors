import pytest
from app.core.redis import RedisCache


@pytest.mark.asyncio
async def test_redis_set_and_get(test_cache: RedisCache):
    """
    Test Redis set and get operations
    """
    key = "test_key"
    value = {"data": "test_value", "number": 42}

    # Set value
    result = await test_cache.set(key, value, ttl=60)
    assert result is True

    # Get value
    retrieved = await test_cache.get(key)
    assert retrieved == value


@pytest.mark.asyncio
async def test_redis_exists(test_cache: RedisCache):
    """
    Test Redis exists operation
    """
    key = "test_exists"
    value = {"test": "data"}

    # Key doesn't exist
    exists = await test_cache.exists(key)
    assert exists is False

    # Set key
    await test_cache.set(key, value)

    # Key exists
    exists = await test_cache.exists(key)
    assert exists is True


@pytest.mark.asyncio
async def test_redis_delete(test_cache: RedisCache):
    """
    Test Redis delete operation
    """
    key = "test_delete"
    value = {"test": "data"}

    # Set key
    await test_cache.set(key, value)
    assert await test_cache.exists(key) is True

    # Delete key
    result = await test_cache.delete(key)
    assert result is True

    # Key no longer exists
    assert await test_cache.exists(key) is False


@pytest.mark.asyncio
async def test_redis_get_nonexistent_key(test_cache: RedisCache):
    """
    Test getting a non-existent key returns None
    """
    result = await test_cache.get("nonexistent_key")
    assert result is None


@pytest.mark.asyncio
async def test_redis_clear_pattern(test_cache: RedisCache):
    """
    Test clearing keys by pattern
    """
    # Set multiple keys with pattern
    await test_cache.set("stock:AAPL", {"price": 150})
    await test_cache.set("stock:GOOGL", {"price": 2800})
    await test_cache.set("news:tech", {"title": "Tech News"})

    # Clear stock keys
    deleted_count = await test_cache.clear_pattern("stock:*")
    assert deleted_count == 2

    # Verify stock keys are deleted
    assert await test_cache.exists("stock:AAPL") is False
    assert await test_cache.exists("stock:GOOGL") is False

    # Verify news key still exists
    assert await test_cache.exists("news:tech") is True


@pytest.mark.asyncio
async def test_redis_set_with_custom_ttl(test_cache: RedisCache):
    """
    Test setting value with custom TTL
    """
    key = "test_ttl"
    value = {"data": "test"}
    custom_ttl = 120

    result = await test_cache.set(key, value, ttl=custom_ttl)
    assert result is True

    # Verify key exists
    assert await test_cache.exists(key) is True


@pytest.mark.asyncio
async def test_redis_connect_disconnect():
    """
    Test Redis connect and disconnect
    """
    cache = RedisCache()
    assert cache.redis is None

    await cache.connect()
    assert cache.redis is not None

    await cache.disconnect()
