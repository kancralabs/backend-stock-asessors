# ⚡ Quick Start Guide

## 🐳 Docker (Recommended)

```bash
# 1. Clone & setup
cd backend-stock-asessors
cp .env.example .env

# 2. Start everything
docker-compose up -d

# 3. Check logs
docker-compose logs -f api

# 4. Test API
curl http://localhost:8000/api/v1/health
```

**URLs:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## 💻 Local Development

```bash
# 1. Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
make install

# 3. Setup environment
cp .env.example .env
# Edit .env with your settings

# 4. Start services (Docker)
docker-compose up -d postgres redis

# 5. Run API
make dev
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage (requires 80%+)
make coverage

# View coverage report
open htmlcov/index.html
```

## 🎨 Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Clean cache
make clean
```

## 🔍 Useful Commands

```bash
# Check health
curl http://localhost:8000/api/v1/health

# Check version
curl http://localhost:8000

# Ping
curl http://localhost:8000/api/v1/ping

# View logs
docker-compose logs -f api

# Restart services
docker-compose restart

# Stop everything
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 📦 Database

```bash
# Access PostgreSQL
docker exec -it stock_assessor_db psql -U postgres -d stock_assessor

# Run migrations (when ready)
# alembic upgrade head

# Create migration
# alembic revision --autogenerate -m "description"
```

## 🗄️ Redis

```bash
# Access Redis CLI
docker exec -it stock_assessor_redis redis-cli

# Check keys
docker exec -it stock_assessor_redis redis-cli KEYS "*"

# Flush cache
docker exec -it stock_assessor_redis redis-cli FLUSHDB
```

## 🐛 Troubleshooting

### Port already in use?
```bash
# Check what's using the port
lsof -i :8000
lsof -i :5432
lsof -i :6379

# Change ports in docker-compose.yml
```

### Database connection error?
```bash
# Check if PostgreSQL is running
docker-compose ps

# Check logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres
```

### Redis connection error?
```bash
# Check if Redis is running
docker-compose ps

# Test connection
docker exec -it stock_assessor_redis redis-cli PING

# Restart Redis
docker-compose restart redis
```

### Tests failing?
```bash
# Make sure services are running
docker-compose up -d postgres redis

# Check if test database exists
docker exec -it stock_assessor_db psql -U postgres -l

# Run tests with verbose output
pytest -vv

# Run single test
pytest tests/test_main.py::test_root_endpoint -v
```

## 📊 Monitoring

```bash
# Watch logs
docker-compose logs -f

# Check resource usage
docker stats

# Check container health
docker-compose ps
```

## 🚀 Production Deploy

```bash
# Build production image
docker build -t stock-assessor-api:latest .

# Run production
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  stock-assessor-api:latest
```

## 📚 More Info

- [README.md](README.md) - Full documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide
- [CI_CD_SETUP.md](CI_CD_SETUP.md) - CI/CD setup
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview

## 🆘 Help

```bash
# Show make commands
make help

# Check Python version
python --version

# Check Docker version
docker --version
docker-compose --version
```

---

**Ready to code!** 🎉
