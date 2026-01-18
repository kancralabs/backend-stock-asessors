# 📦 Dependencies Management

## Overview

Project ini menggunakan dua file requirements untuk memisahkan production dan development dependencies.

## Files

### `requirements.txt` - Production Dependencies
File ini berisi **hanya** dependencies yang dibutuhkan untuk menjalankan aplikasi di production.

```bash
# Install production dependencies
pip install -r requirements.txt
```

**Includes:**
- FastAPI & Uvicorn
- Database (SQLAlchemy, PostgreSQL, Alembic)
- Redis cache
- HTTP client (httpx)
- Data processing (Pandas, NumPy)
- Schedulers (APScheduler, Celery)
- Telegram bot
- Utilities

### `requirements-dev.txt` - Development Dependencies
File ini berisi **semua** dependencies termasuk tools untuk development, testing, dan code quality.

```bash
# Install dev dependencies (includes production deps)
pip install -r requirements-dev.txt
```

**Additional includes:**
- Testing (pytest, pytest-cov, coverage)
- Code quality (Black, Flake8, isort, mypy)
- Pre-commit hooks
- Security scanning (Bandit)
- Type stubs

## Installation

### For Development
```bash
# Recommended: use make command
make setup

# Or manually
pip install -r requirements-dev.txt
pre-commit install
```

### For Production
```bash
pip install -r requirements.txt
```

### Using Docker
```bash
# Docker will automatically use requirements.txt
docker-compose up -d
```

## Version Pinning Strategy

We use **compatible release specifiers** to allow minor updates while preventing breaking changes:

```python
# Format: package>=min_version,<max_version
fastapi>=0.109.0,<0.110.0  # Allow 0.109.x patches
```

**Benefits:**
- ✅ Get security patches automatically
- ✅ Prevent breaking changes
- ✅ Reproducible builds
- ✅ Easy to update

## Key Dependencies

### Core Framework
| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | >=0.109.0,<0.110.0 | Web framework |
| uvicorn | >=0.27.0,<0.28.0 | ASGI server |
| pydantic | >=2.5.0,<3.0.0 | Data validation |

### Database
| Package | Version | Purpose |
|---------|---------|---------|
| sqlalchemy | >=2.0.25,<2.1.0 | ORM |
| asyncpg | >=0.29.0,<0.30.0 | Async PostgreSQL driver |
| alembic | >=1.13.0,<2.0.0 | Migrations |

### Cache & Queue
| Package | Version | Purpose |
|---------|---------|---------|
| redis | >=5.0.0,<6.0.0 | Cache & session store |
| celery[redis] | >=5.3.0,<6.0.0 | Task queue |

### Data Processing
| Package | Version | Purpose |
|---------|---------|---------|
| pandas | >=2.1.0,<3.0.0 | Data manipulation |
| numpy | >=1.26.0,<2.0.0 | Numerical computing |

### External APIs
| Package | Version | Purpose |
|---------|---------|---------|
| httpx | >=0.25.0,<0.27.0 | HTTP client |
| python-telegram-bot | >=20.7,<21.0 | Telegram integration |

## Dependency Conflicts

### httpx Version Conflict
**Issue:** `python-telegram-bot` requires `httpx~=0.25.2`

**Solution:**
```python
# Use compatible range
httpx>=0.25.0,<0.27.0
```

This allows both packages to use httpx 0.25.x or 0.26.x.

## Updating Dependencies

### Check for Updates
```bash
# Check outdated packages
pip list --outdated

# Or use pip-review (install first)
pip install pip-review
pip-review
```

### Update Specific Package
```bash
# Update within version constraints
pip install --upgrade fastapi

# Test after update
make test
```

### Update All Packages
```bash
# Create backup
cp requirements.txt requirements.txt.backup
cp requirements-dev.txt requirements-dev.txt.backup

# Update all (careful!)
pip install --upgrade -r requirements-dev.txt

# Test thoroughly
make test
make coverage
make lint
```

### Update Version Constraints
When a new major version is released:

1. **Check changelog** for breaking changes
2. **Update version range** in requirements files
3. **Test thoroughly**
4. **Update code** if needed
5. **Commit changes**

Example:
```python
# Before
fastapi>=0.109.0,<0.110.0

# After (when 0.110 is tested)
fastapi>=0.110.0,<0.111.0
```

## Security Updates

### Check for Vulnerabilities
```bash
# Using pip-audit
pip install pip-audit
pip-audit

# Using safety
pip install safety
safety check
```

### Apply Security Patches
```bash
# Update package with security fix
pip install --upgrade <package>

# Verify fix
pip-audit

# Test
make test
```

## Adding New Dependencies

### 1. Determine Category
- **Production**: Required to run the app
- **Development**: Only needed for development/testing

### 2. Install and Test
```bash
# Install package
pip install <package>

# Test the app
make test
```

### 3. Add to Requirements File

**For production dependency:**
```bash
# Add to requirements.txt
echo "<package>>=X.Y.0,<X.(Y+1).0" >> requirements.txt
```

**For dev dependency:**
```bash
# Add to requirements-dev.txt
echo "<package>>=X.Y.0,<X.(Y+1).0" >> requirements-dev.txt
```

### 4. Update Lock File (Optional)
If using pip-tools:
```bash
pip-compile requirements.txt
pip-compile requirements-dev.txt
```

### 5. Document
Add to this file if it's a significant dependency.

## Best Practices

### ✅ DO
- Use version ranges (>=X.Y,<X.(Y+1))
- Keep requirements files sorted by category
- Test after updating dependencies
- Document significant dependencies
- Use `requirements-dev.txt` for development
- Commit both requirements files

### ❌ DON'T
- Use exact versions (==) unless necessary
- Use loose constraints (>=X.Y)
- Install packages without testing
- Mix dev and prod dependencies
- Commit without updating requirements

## Troubleshooting

### Conflict Resolution

**Error: Package conflicts**
```bash
# Clear cache
pip cache purge

# Reinstall from scratch
pip uninstall -r requirements-dev.txt -y
pip install -r requirements-dev.txt
```

**Error: No matching distribution**
```bash
# Check Python version
python --version

# Update pip
pip install --upgrade pip

# Try with --no-cache-dir
pip install --no-cache-dir -r requirements-dev.txt
```

### Clean Install
```bash
# Remove virtual environment
deactivate
rm -rf venv/

# Create new environment
python -m venv venv
source venv/bin/activate

# Install fresh
pip install --upgrade pip
pip install -r requirements-dev.txt
```

## CI/CD Integration

GitHub Actions automatically installs `requirements-dev.txt` for testing:

```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements-dev.txt
```

Docker uses `requirements.txt` for production image:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
```

## FAQ

**Q: Why two requirements files?**
A: To keep production images lean. Dev tools aren't needed in production.

**Q: Which file for CI/CD?**
A: Use `requirements-dev.txt` for CI/CD to run tests and checks.

**Q: Can I use pip freeze?**
A: Not recommended. We prefer version ranges for flexibility.

**Q: What about requirements.lock?**
A: Consider using pip-tools for lock files in future.

**Q: How to handle conflicts?**
A: Adjust version ranges to find compatible versions.

---

**Last Updated**: 2026-01-18
**Python Version**: 3.11+
**Package Manager**: pip
