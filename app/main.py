from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.endpoints import health
from app.db.session import engine
from app.db.base import Base
from app.core.redis import cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    # Startup
    print("🚀 Starting up Stock Assessor Backend...")
    print(f"📝 Environment: {settings.ENVIRONMENT}")
    print(f"🗄️  Database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'configured'}")

    # Connect to Redis
    try:
        await cache.connect()
    except Exception as e:
        print(f"⚠️  Redis connection failed: {e}")

    # Create database tables (uncomment if needed)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown
    print("🛑 Shutting down Stock Assessor Backend...")
    await cache.disconnect()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Stock Assessment & Analysis Backend - Deterministic, Fast, Scalable",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["health"])


@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Stock Assessor Backend API",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs"
    }
