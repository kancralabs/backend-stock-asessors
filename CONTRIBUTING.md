# Contributing Guide

## Setup Development Environment

1. **Clone repository**
```bash
git clone <repository-url>
cd backend-stock-asessors
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
make install
# or
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Start services**
```bash
make docker-up
```

## Development Workflow

### 1. Create a branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make changes
- Write code following the project's style guide
- Add tests for new features
- Update documentation if needed

### 3. Run tests
```bash
# Run all tests
make test

# Run with coverage
make coverage

# Coverage must be >= 80%
```

### 4. Format and lint
```bash
# Format code
make format

# Check linting
make lint
```

### 5. Commit changes
```bash
git add .
git commit -m "feat: add new feature"
# or
git commit -m "fix: fix bug in X"
```

**Commit message conventions:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### 6. Push and create PR
```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style

- Follow PEP 8
- Use Black for formatting (line length: 100)
- Use type hints where appropriate
- Write docstrings for functions and classes

## Testing

- Write unit tests for all new features
- Maintain test coverage >= 80%
- Use pytest fixtures for setup
- Mock external dependencies

### Test structure
```python
@pytest.mark.asyncio
async def test_feature_name():
    """
    Test description
    """
    # Arrange
    # ...

    # Act
    # ...

    # Assert
    # ...
```

## CI/CD Pipeline

Every PR will automatically:
1. Run all tests
2. Check code coverage (must be >= 80%)
3. Run linting and format checks
4. Build Docker image
5. Get reviewed by CodeRabbit AI

## Questions?

Open an issue or ask in the discussion board.
