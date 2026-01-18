# 🏗️ Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Stock Assessor System                    │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Telegram   │────▶│   FastAPI    │────▶│   Frontend   │
│     Bot      │     │     API      │     │     App      │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                    ┌───────┴───────┐
                    ▼               ▼
            ┌──────────────┐ ┌──────────────┐
            │  PostgreSQL  │ │    Redis     │
            │   Database   │ │    Cache     │
            └──────────────┘ └──────────────┘
                    │
            ┌───────┴───────┐
            ▼               ▼
    ┌──────────────┐ ┌──────────────┐
    │ Alpha Vantage│ │    GDELT     │
    │     API      │ │     API      │
    └──────────────┘ └──────────────┘
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     Scheduler (APScheduler)                  │
│                    Cron: Every 4 Hours                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────────────┐
    │          Data Fetcher Service               │
    ├─────────────────────────────────────────────┤
    │  • Alpha Vantage Client (Stock Prices)      │
    │  • GDELT Client (News & Sentiment)          │
    │  • Rate Limiting Handler                    │
    │  • Error Handler & Retry Logic              │
    └────────────┬────────────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────────────────┐
    │          Analysis Service                   │
    ├─────────────────────────────────────────────┤
    │  • Technical Indicators Calculator          │
    │    - Moving Averages (SMA, EMA)             │
    │    - RSI, MACD, Bollinger Bands             │
    │  • Sentiment Analyzer                       │
    │  • Market Breadth Calculator                │
    └────────────┬────────────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────────────────┐
    │          PostgreSQL Database                │
    ├─────────────────────────────────────────────┤
    │  Tables:                                    │
    │  • stocks                                   │
    │  • stock_prices (historical)                │
    │  • news_articles                            │
    │  • sentiment_scores                         │
    │  • technical_indicators                     │
    │  • alerts                                   │
    └────────────┬────────────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────────────────┐
    │            Redis Cache                      │
    ├─────────────────────────────────────────────┤
    │  Keys:                                      │
    │  • stock:{symbol}:latest                    │
    │  • stock:{symbol}:indicators                │
    │  • news:{symbol}:sentiment                  │
    │  • market:breadth                           │
    │  TTL: 1 hour (configurable)                │
    └────────────┬────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐  ┌──────────────┐
│  Telegram    │  │   REST API   │
│     Bot      │  │   Endpoint   │
└──────────────┘  └──────────────┘
```

## Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                        │
├─────────────────────────────────────────────────────────────┤
│  • FastAPI Routes (app/api/endpoints/)                      │
│  • Request Validation (Pydantic Schemas)                    │
│  • Response Formatting                                      │
│  • CORS Middleware                                          │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                      │
├─────────────────────────────────────────────────────────────┤
│  • Services (app/services/)                                 │
│    - Data Fetchers                                          │
│    - Analyzers                                              │
│    - Calculators                                            │
│  • Business Rules                                           │
│  • Domain Logic                                             │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
├─────────────────────────────────────────────────────────────┤
│  • SQLAlchemy Models (app/models/)                          │
│  • Database Session Management                              │
│  • Repository Pattern                                       │
│  • Redis Cache Manager                                      │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                       │
├─────────────────────────────────────────────────────────────┤
│  • PostgreSQL Database                                      │
│  • Redis Cache                                              │
│  • External APIs (Alpha Vantage, GDELT)                     │
│  • Message Queue (optional)                                 │
└─────────────────────────────────────────────────────────────┘
```

## API Request Flow

```
Client Request
      │
      ▼
┌──────────────────┐
│  CORS Middleware │  ← Check origin
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Rate Limiter     │  ← Check rate limits
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  FastAPI Router  │  ← Route to endpoint
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Schema Validator │  ← Validate request
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Redis Check     │  ← Check cache
└────────┬─────────┘
         │
     ┌───┴───┐
     │ Hit?  │
     └───┬───┘
     Yes │   No
         │   │
         │   ▼
         │ ┌──────────────────┐
         │ │  Service Layer   │
         │ └────────┬─────────┘
         │          │
         │          ▼
         │ ┌──────────────────┐
         │ │  Database Query  │
         │ └────────┬─────────┘
         │          │
         │          ▼
         │ ┌──────────────────┐
         │ │  Cache Result    │
         │ └────────┬─────────┘
         │          │
         └──────────┘
                │
                ▼
         ┌──────────────────┐
         │ Format Response  │
         └────────┬─────────┘
                  │
                  ▼
            Client Response
```

## Caching Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                    Redis Cache Layers                        │
└─────────────────────────────────────────────────────────────┘

Layer 1: Hot Data (TTL: 5 minutes)
├─ Latest stock prices
├─ Real-time market data
└─ Current sentiment scores

Layer 2: Warm Data (TTL: 1 hour)
├─ Technical indicators
├─ Aggregated news
└─ Market breadth

Layer 3: Cold Data (TTL: 24 hours)
├─ Historical analysis
├─ Long-term trends
└─ Statistical summaries

Cache Invalidation:
• On data update → Clear specific keys
• On error → Keep stale data, log error
• On schedule → Refresh proactively
```

## Database Schema (Future)

```
┌─────────────────────────────────────────────────────────────┐
│                      stocks                                  │
├─────────────────────────────────────────────────────────────┤
│ id (PK)              │ UUID                                  │
│ symbol               │ VARCHAR(10)                           │
│ name                 │ VARCHAR(255)                          │
│ exchange             │ VARCHAR(50)                           │
│ sector               │ VARCHAR(100)                          │
│ created_at           │ TIMESTAMP                             │
│ updated_at           │ TIMESTAMP                             │
└─────────────────────────────────────────────────────────────┘
                         │
                         │ 1:N
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   stock_prices                               │
├─────────────────────────────────────────────────────────────┤
│ id (PK)              │ UUID                                  │
│ stock_id (FK)        │ UUID                                  │
│ date                 │ DATE                                  │
│ open                 │ DECIMAL(10,2)                         │
│ high                 │ DECIMAL(10,2)                         │
│ low                  │ DECIMAL(10,2)                         │
│ close                │ DECIMAL(10,2)                         │
│ volume               │ BIGINT                                │
│ created_at           │ TIMESTAMP                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   news_articles                              │
├─────────────────────────────────────────────────────────────┤
│ id (PK)              │ UUID                                  │
│ stock_id (FK)        │ UUID                                  │
│ title                │ TEXT                                  │
│ url                  │ TEXT                                  │
│ published_at         │ TIMESTAMP                             │
│ sentiment_score      │ DECIMAL(5,4)                          │
│ source               │ VARCHAR(100)                          │
│ created_at           │ TIMESTAMP                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                technical_indicators                          │
├─────────────────────────────────────────────────────────────┤
│ id (PK)              │ UUID                                  │
│ stock_id (FK)        │ UUID                                  │
│ date                 │ DATE                                  │
│ sma_20               │ DECIMAL(10,2)                         │
│ sma_50               │ DECIMAL(10,2)                         │
│ rsi                  │ DECIMAL(5,2)                          │
│ macd                 │ DECIMAL(10,4)                         │
│ bb_upper             │ DECIMAL(10,2)                         │
│ bb_lower             │ DECIMAL(10,2)                         │
│ created_at           │ TIMESTAMP                             │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack Details

### Backend Framework
- **FastAPI**: Modern, fast, async Python web framework
- **Uvicorn**: ASGI server for production

### Database
- **PostgreSQL 15**: Primary data store
- **SQLAlchemy 2.0**: ORM with async support
- **Alembic**: Database migrations

### Cache
- **Redis 7**: In-memory cache with persistence
- **redis-py**: Async Redis client

### Data Processing
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing

### Task Scheduling
- **APScheduler**: Cron-like scheduler
- **Celery**: Distributed task queue (optional)

### External APIs
- **Alpha Vantage**: Stock market data
- **GDELT**: Global news & sentiment
- **httpx**: Async HTTP client

### Testing
- **pytest**: Testing framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting

### Code Quality
- **Black**: Code formatter
- **Flake8**: Linter
- **mypy**: Type checker
- **isort**: Import sorter

### CI/CD
- **GitHub Actions**: CI/CD pipeline
- **Codecov**: Coverage reporting
- **CodeRabbit**: AI code review

### Containerization
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## Performance Considerations

### Caching Strategy
- Redis-first approach for frequently accessed data
- Layered cache with different TTLs
- Proactive cache warming

### Database Optimization
- Proper indexing on frequently queried columns
- Connection pooling
- Query optimization with SQLAlchemy

### Async Operations
- All I/O operations are async
- Concurrent API calls when possible
- Non-blocking database queries

### Rate Limiting
- Respect API rate limits (Alpha Vantage: 5/min)
- Exponential backoff for retries
- Request queuing

## Security

### API Security
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention (SQLAlchemy ORM)

### Secrets Management
- Environment variables for sensitive data
- No hardcoded credentials
- .env files excluded from git

### Data Protection
- PostgreSQL user permissions
- Redis password protection (production)
- HTTPS for external API calls

## Scalability

### Horizontal Scaling
- Stateless API design
- Shared cache (Redis)
- Load balancer ready

### Vertical Scaling
- Async/await for better resource usage
- Connection pooling
- Efficient caching

### Future Enhancements
- Message queue for background jobs
- Microservices architecture
- Read replicas for database
- CDN for static content

---

**Architecture Version**: 1.0
**Last Updated**: 2026-01-18
**Status**: Foundation Complete
