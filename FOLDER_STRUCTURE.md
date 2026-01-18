# 📁 Folder Structure Documentation

## Overview

```
backend-stock-asessors/
├── 📁 .github/              # GitHub specific files
├── 📁 app/                  # Main application code
├── 📁 tests/                # Test files
├── 📄 Configuration files
└── 📄 Documentation files
```

## Detailed Structure

```
backend-stock-asessors/
│
├── 📁 .github/
│   ├── workflows/
│   │   └── ci.yml                    # CI/CD pipeline configuration
│   └── PULL_REQUEST_TEMPLATE.md      # PR template
│
├── 📁 app/                            # Main application package
│   │
│   ├── 📄 __init__.py                # Package initialization
│   ├── 📄 main.py                    # FastAPI app entry point
│   │
│   ├── 📁 api/                       # API layer
│   │   ├── __init__.py
│   │   ├── endpoints/                # API endpoints
│   │   │   ├── __init__.py
│   │   │   └── health.py            # Health check endpoints
│   │   └── deps/                     # Dependencies (future)
│   │
│   ├── 📁 core/                      # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py                # Configuration settings
│   │   └── redis.py                 # Redis cache manager
│   │
│   ├── 📁 db/                        # Database layer
│   │   ├── __init__.py
│   │   ├── base.py                  # SQLAlchemy base
│   │   └── session.py               # Database session
│   │
│   ├── 📁 models/                    # SQLAlchemy models (future)
│   │   └── __init__.py
│   │
│   ├── 📁 schemas/                   # Pydantic schemas (future)
│   │   └── __init__.py
│   │
│   └── 📁 services/                  # Business logic (future)
│       └── __init__.py
│
├── 📁 tests/                          # Test files
│   ├── __init__.py
│   ├── conftest.py                   # Pytest fixtures & config
│   ├── test_main.py                  # API endpoint tests
│   ├── test_config.py                # Configuration tests
│   ├── test_redis.py                 # Redis operations tests
│   ├── test_database.py              # Database tests
│   └── test_health.py                # Health check tests
│
├── 📄 .coderabbit.yaml               # CodeRabbit configuration
├── 📄 .coveragerc                    # Coverage configuration
├── 📄 .env.example                   # Environment variables template
├── 📄 .flake8                        # Flake8 linting rules
├── 📄 .gitignore                     # Git ignore rules
├── 📄 codecov.yml                    # Codecov configuration
├── 📄 docker-compose.yml             # Docker Compose setup
├── 📄 Dockerfile                     # Docker image definition
├── 📄 Makefile                       # Helper commands
├── 📄 pytest.ini                     # Pytest configuration
├── 📄 pyproject.toml                 # Python project config
├── 📄 requirements.txt               # Python dependencies
│
└── 📄 Documentation Files
    ├── README.md                     # Main documentation
    ├── ARCHITECTURE.md               # Architecture documentation
    ├── CI_CD_SETUP.md               # CI/CD setup guide
    ├── CONTRIBUTING.md              # Contributing guidelines
    ├── FOLDER_STRUCTURE.md          # This file
    ├── PROJECT_SUMMARY.md           # Project summary
    ├── QUICK_START.md               # Quick start guide
    └── SETUP_COMPLETE.md            # Setup completion checklist
```

## Directory Purposes

### 📁 `.github/`
GitHub-specific files for CI/CD and templates.

**When to use:**
- Add workflow files for GitHub Actions
- Add issue/PR templates
- Add GitHub-specific automation

**Examples:**
```
.github/
├── workflows/
│   ├── ci.yml          # Main CI/CD
│   ├── deploy.yml      # Deployment
│   └── security.yml    # Security scans
└── ISSUE_TEMPLATE.md
```

### 📁 `app/`
Main application code. All production code goes here.

**Structure:**
- **Modular**: Each folder has specific purpose
- **Layered**: Separation of concerns
- **Scalable**: Easy to add new features

### 📁 `app/api/`
API layer - handles HTTP requests and responses.

**Purpose:**
- Define API endpoints
- Request validation
- Response formatting
- Route organization

**Future structure:**
```
app/api/
├── endpoints/
│   ├── stocks.py       # Stock endpoints
│   ├── news.py         # News endpoints
│   ├── analysis.py     # Analysis endpoints
│   └── alerts.py       # Alert endpoints
└── deps/
    ├── auth.py         # Authentication
    └── permissions.py  # Authorization
```

### 📁 `app/core/`
Core functionality - shared utilities and configs.

**Contains:**
- Configuration management
- Cache managers
- Logging setup
- Common utilities

**Future additions:**
```
app/core/
├── config.py           # Settings
├── redis.py            # Redis cache
├── security.py         # Security utils
├── logging.py          # Logging config
└── exceptions.py       # Custom exceptions
```

### 📁 `app/db/`
Database layer - all database related code.

**Contains:**
- Database connections
- Session management
- Base models
- Database utilities

**Future additions:**
```
app/db/
├── base.py             # SQLAlchemy base
├── session.py          # Session management
├── repositories/       # Repository pattern
└── migrations/         # Alembic migrations
```

### 📁 `app/models/`
SQLAlchemy models - database table definitions.

**Example structure:**
```
app/models/
├── __init__.py
├── stock.py            # Stock model
├── price.py            # Price history model
├── news.py             # News model
├── indicator.py        # Technical indicators model
└── user.py             # User model (if needed)
```

**Model example:**
```python
# app/models/stock.py
from sqlalchemy import Column, String, DateTime
from app.db.base import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(String, primary_key=True)
    symbol = Column(String(10), unique=True)
    name = Column(String(255))
    exchange = Column(String(50))
```

### 📁 `app/schemas/`
Pydantic schemas - request/response validation.

**Example structure:**
```
app/schemas/
├── __init__.py
├── stock.py            # Stock schemas
├── price.py            # Price schemas
├── news.py             # News schemas
└── analysis.py         # Analysis schemas
```

**Schema example:**
```python
# app/schemas/stock.py
from pydantic import BaseModel

class StockBase(BaseModel):
    symbol: str
    name: str
    exchange: str

class StockCreate(StockBase):
    pass

class StockResponse(StockBase):
    id: str

    class Config:
        from_attributes = True
```

### 📁 `app/services/`
Business logic - core functionality implementation.

**Example structure:**
```
app/services/
├── __init__.py
├── alpha_vantage.py    # Alpha Vantage client
├── gdelt.py            # GDELT client
├── analyzer.py         # Technical analysis
├── sentiment.py        # Sentiment analysis
└── scheduler.py        # Task scheduling
```

**Service example:**
```python
# app/services/alpha_vantage.py
import httpx
from app.core.config import settings

class AlphaVantageService:
    def __init__(self):
        self.api_key = settings.ALPHA_VANTAGE_API_KEY
        self.base_url = settings.ALPHA_VANTAGE_BASE_URL

    async def get_stock_price(self, symbol: str):
        # Implementation
        pass
```

### 📁 `tests/`
Test files - mirrors app structure.

**Best practices:**
- One test file per module
- Test file name: `test_<module>.py`
- Fixtures in `conftest.py`
- Mark tests: `@pytest.mark.unit`, `@pytest.mark.integration`

**Future structure:**
```
tests/
├── conftest.py
├── unit/
│   ├── test_services.py
│   ├── test_models.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   ├── test_database.py
│   └── test_redis.py
└── e2e/
    └── test_workflows.py
```

## File Naming Conventions

### Python Files
- **Models**: Singular noun, e.g., `stock.py`, `user.py`
- **Services**: Descriptive, e.g., `alpha_vantage.py`, `analyzer.py`
- **Endpoints**: Plural noun, e.g., `stocks.py`, `users.py`
- **Tests**: Prefix with `test_`, e.g., `test_stock.py`

### Configuration Files
- **Hidden files**: Start with `.`, e.g., `.env`, `.gitignore`
- **YAML/YML**: Lowercase, e.g., `docker-compose.yml`
- **Markdown**: UPPERCASE, e.g., `README.md`, `CONTRIBUTING.md`

## Adding New Features

### Example: Adding Stock Endpoints

1. **Create model**
```bash
# app/models/stock.py
```

2. **Create schema**
```bash
# app/schemas/stock.py
```

3. **Create service**
```bash
# app/services/stock_service.py
```

4. **Create endpoint**
```bash
# app/api/endpoints/stocks.py
```

5. **Create tests**
```bash
# tests/test_stocks.py
```

6. **Register router**
```python
# app/main.py
from app.api.endpoints import stocks
app.include_router(stocks.router, prefix="/api/v1", tags=["stocks"])
```

## Best Practices

### 1. Keep It Organized
- One class/function per purpose
- Related code stays together
- Clear naming conventions

### 2. Separation of Concerns
- **Models**: Data structure only
- **Schemas**: Validation only
- **Services**: Business logic only
- **Endpoints**: HTTP handling only

### 3. DRY (Don't Repeat Yourself)
- Shared code in `app/core/`
- Reusable functions in utilities
- Common patterns in base classes

### 4. Testing
- Test files mirror app structure
- Fixtures for common setups
- Mock external dependencies

### 5. Documentation
- Docstrings for all public functions
- README for each major module
- Keep docs updated

## Common Patterns

### Adding New Endpoint
```
1. Model (if needed)     → app/models/
2. Schema                → app/schemas/
3. Service               → app/services/
4. Endpoint              → app/api/endpoints/
5. Tests                 → tests/
6. Register in main.py
```

### Adding External API
```
1. Client service        → app/services/
2. Configuration         → app/core/config.py
3. Tests with mocks      → tests/
4. Document in README
```

### Adding Background Job
```
1. Job function          → app/services/scheduler.py
2. Schedule config       → app/core/config.py
3. Register in main.py
4. Tests                 → tests/
```

## Quick Reference

| Need to...                | Go to...                    |
|---------------------------|----------------------------|
| Add API endpoint          | `app/api/endpoints/`       |
| Add database model        | `app/models/`              |
| Add validation schema     | `app/schemas/`             |
| Add business logic        | `app/services/`            |
| Add configuration         | `app/core/config.py`       |
| Add tests                 | `tests/`                   |
| Add dependencies          | `requirements.txt`         |
| Add documentation         | Root `*.md` files          |
| Add CI/CD workflow        | `.github/workflows/`       |

---

**Last Updated**: 2026-01-18
**Status**: Foundation Complete
