# Stock Assessor Backend API

![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/kancralabs/backend-stock-asessors?utm_source=oss&utm_medium=github&utm_campaign=kancralabs%2Fbackend-stock-asessors&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)


![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Coverage](https://img.shields.io/badge/coverage-80%25+-brightgreen.svg)

A deterministic, fast, and scalable stock analysis backend built with FastAPI.

> 📝 **Note**: Setelah push ke GitHub, tambahkan badges untuk CI/CD dan Codecov. Lihat [CI_CD_SETUP.md](CI_CD_SETUP.md) untuk instruksi lengkap.

## Features

- FastAPI with async support
- PostgreSQL for data persistence
- Redis for caching
- Alpha Vantage integration for stock data
- GDELT integration for news sentiment
- Telegram bot integration
- Docker support

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL + SQLAlchemy 2.0
- **Cache**: Redis
- **Data Processing**: Pandas, NumPy
- **Scheduler**: APScheduler / Celery Beat
- **Bot**: python-telegram-bot

## Quick Start

### 1. Clone and Setup

```bash
cd backend-stock-asessors
cp .env.example .env
# Edit .env with your API keys
```

### 2. Using Docker (Recommended)

```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`

### 3. Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run PostgreSQL and Redis
# Make sure they are running on localhost

# Run the application
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

## Project Structure

```
backend-stock-asessors/
├── app/
│   ├── api/
│   │   ├── endpoints/      # API route handlers
│   │   └── deps/           # Dependencies
│   ├── core/               # Core configurations
│   │   ├── config.py       # Settings
│   │   └── redis.py        # Redis cache manager
│   ├── db/                 # Database
│   │   ├── base.py         # Base model
│   │   └── session.py      # DB session
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   └── main.py             # FastAPI app
├── tests/                  # Tests
├── alembic/                # Database migrations
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Health Check

```bash
curl http://localhost:8000/api/v1/health
```

## Development

```bash
# Run with hot reload
uvicorn app.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Format code
black app/

# Lint
flake8 app/
```

## CI/CD

This project uses GitHub Actions for continuous integration and deployment:

- **Test & Coverage**: Runs all tests with 80% minimum coverage requirement
- **Lint & Format**: Checks code formatting and linting
- **Build**: Builds Docker image

### Required GitHub Secrets

For CI/CD to work properly, add these secrets to your GitHub repository:

- `CODECOV_TOKEN`: Token for uploading coverage to Codecov

### Integrations

- **Codecov**: Automatic coverage reporting on every PR
- **CodeRabbit**: AI-powered code review in Bahasa Indonesia

## Goals

- **Stable**: No rate limiting issues
- **Deterministic**: No LLM hallucinations
- **Fast**: Redis-first caching
- **Scalable**: Ready for horizontal scaling