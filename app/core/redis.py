from redis.asyncio import Redis
from typing import Optional
import json

from app.core.config import settings


class RedisCache:
    """
    Redis cache manager for fast data access
    """

    def __init__(self):
        self.redis: Optional[Redis] = None

    async def connect(self):
        """
        Connect to Redis
        """
        self.redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_keepalive=True,
        )
        await self.redis.ping()
        print(f"✅ Redis connected: {settings.REDIS_HOST}:{settings.REDIS_PORT}")

    async def disconnect(self):
        """
        Disconnect from Redis
        """
        if self.redis:
            await self.redis.close()
            print("🔌 Redis disconnected")

    async def get(self, key: str) -> Optional[dict]:
        """
        Get value from cache
        """
        if not self.redis:
            return None

        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: dict, ttl: int = None) -> bool:
        """
        Set value in cache with TTL
        """
        if not self.redis:
            return False

        ttl = ttl or settings.REDIS_CACHE_TTL
        await self.redis.setex(
            key,
            ttl,
            json.dumps(value, default=str)
        )
        return True

    async def delete(self, key: str) -> bool:
        """
        Delete key from cache
        """
        if not self.redis:
            return False

        await self.redis.delete(key)
        return True

    async def exists(self, key: str) -> bool:
        """
        Check if key exists
        """
        if not self.redis:
            return False

        return await self.redis.exists(key) > 0

    async def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching pattern
        """
        if not self.redis:
            return 0

        keys = await self.redis.keys(pattern)
        if keys:
            return await self.redis.delete(*keys)
        return 0


# Global cache instance
cache = RedisCache()


async def get_cache() -> RedisCache:
    """
    Dependency for getting cache instance
    """
    return cache
