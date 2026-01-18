from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import get_db
from app.core.redis import get_cache, RedisCache

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db), cache: RedisCache = Depends(get_cache)):
    """
    Health check endpoint - checks database and Redis connectivity
    """
    health_status = {"status": "healthy", "database": "disconnected", "redis": "disconnected"}

    # Check database
    try:
        result = await db.execute(text("SELECT 1"))
        if result:
            health_status["database"] = "connected"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["database"] = f"error: {str(e)}"

    # Check Redis
    try:
        if cache.redis:
            await cache.redis.ping()
            health_status["redis"] = "connected"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["redis"] = f"error: {str(e)}"

    return health_status


@router.get("/ping")
async def ping():
    """
    Simple ping endpoint
    """
    return {"message": "pong"}
