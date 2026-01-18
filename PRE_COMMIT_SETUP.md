# 🪝 Pre-commit Setup Guide

## What is Pre-commit?

Pre-commit adalah tool yang menjalankan checks otomatis sebelum kamu commit code. Ini memastikan code kamu selalu:
- ✅ Properly formatted (Black)
- ✅ Imports sorted (isort)
- ✅ Linted (Flake8)
- ✅ Secure (Bandit)
- ✅ No trailing whitespace
- ✅ Valid YAML/JSON

## Installation

### 1. Install Dependencies

```bash
cd backend-stock-asessors

# Install pre-commit
pip install pre-commit

# Or install all requirements
pip install -r requirements.txt
```

### 2. Install Git Hooks

```bash
# Install the pre-commit hooks
pre-commit install

# Install for commit messages (optional)
pre-commit install --hook-type commit-msg
```

Output:
```
pre-commit installed at .git/hooks/pre-commit
```

### 3. Test Installation

```bash
# Run against all files
pre-commit run --all-files
```

## Usage

### Automatic (Recommended)

Pre-commit akan otomatis run setiap kali kamu `git commit`:

```bash
git add .
git commit -m "feat: add new feature"
# Pre-commit hooks akan run otomatis
```

Jika ada error, commit akan dibatalkan dan kamu harus fix issues dulu.

### Manual

Run pre-commit manual tanpa commit:

```bash
# Run on all files
pre-commit run --all-files

# Run on specific files
pre-commit run --files app/main.py

# Run specific hook
pre-commit run black --all-files
pre-commit run flake8 --all-files
```

## Hooks yang Dijalankan

### 1. **Trailing Whitespace**
Removes whitespace di akhir baris.

### 2. **End of File Fixer**
Ensures file berakhir dengan newline.

### 3. **Check YAML**
Validates YAML files syntax.

### 4. **Check JSON**
Validates JSON files syntax.

### 5. **Check Large Files**
Prevents commit files > 1MB.

### 6. **Detect Private Key**
Warns jika ada private key di code.

### 7. **isort**
Sorts Python imports.

```python
# Before
import os
import sys
from app.core import config
from fastapi import FastAPI

# After
import os
import sys

from fastapi import FastAPI

from app.core import config
```

### 8. **Black**
Formats Python code.

```python
# Before
def hello(   name  ):
    return f"Hello, {name}"

# After
def hello(name):
    return f"Hello, {name}"
```

### 9. **Flake8**
Lints Python code.

Checks for:
- Unused imports
- Undefined variables
- Code style issues

### 10. **Bandit**
Security vulnerability scanner.

Checks for:
- Hardcoded passwords
- SQL injection risks
- Use of insecure functions

### 11. **Hadolint**
Lints Dockerfile.

## Common Issues & Solutions

### Issue 1: Pre-commit Fails

```bash
# Error
[ERROR] An error has occurred: CalledProcessError: command returned 1
```

**Solution:**
```bash
# Update pre-commit
pre-commit autoupdate

# Clean cache
pre-commit clean

# Reinstall
pre-commit uninstall
pre-commit install
```

### Issue 2: Black/isort Conflicts

Pre-commit config sudah set isort to be compatible dengan Black.

**If still conflicts:**
```bash
# Run manually in order
isort app/
black app/
```

### Issue 3: Want to Skip Hooks

```bash
# Skip all hooks (not recommended)
git commit --no-verify -m "message"

# Skip specific hook (use SKIP env)
SKIP=flake8 git commit -m "message"
```

### Issue 4: Too Slow

```bash
# Run only on changed files (default)
pre-commit run

# Skip expensive hooks in development
SKIP=mypy,bandit git commit -m "message"
```

## Configuration Files

### `.pre-commit-config.yaml`
Main configuration file for pre-commit hooks.

### `pyproject.toml`
Configuration for:
- Black
- isort
- mypy
- Coverage
- Bandit

### `.flake8`
Configuration for Flake8 linter.

## Best Practices

### 1. Run Before Commit
```bash
# Check your changes before committing
pre-commit run --files $(git diff --name-only --cached)
```

### 2. Update Hooks Regularly
```bash
# Update to latest versions
pre-commit autoupdate
```

### 3. Use in CI/CD
Pre-commit sudah included di GitHub Actions workflow.

### 4. Team Consistency
Semua team member harus install pre-commit untuk consistency.

## Commands Cheat Sheet

```bash
# Installation
pip install pre-commit
pre-commit install

# Run hooks
pre-commit run --all-files              # All files
pre-commit run --files app/main.py      # Specific file
pre-commit run black                    # Specific hook

# Update
pre-commit autoupdate                   # Update hooks

# Maintenance
pre-commit clean                        # Clean cache
pre-commit uninstall                    # Uninstall hooks

# Skip (not recommended)
git commit --no-verify                  # Skip all
SKIP=flake8 git commit                  # Skip specific
```

## IDE Integration

### VS Code

Install extensions:
- **Black Formatter**
- **isort**
- **Flake8**

Add to `.vscode/settings.json`:
```json
{
  "python.formatting.provider": "black",
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

### PyCharm

1. Settings → Tools → External Tools
2. Add Black, isort, flake8 as external tools
3. Enable format on save

## Troubleshooting

### Cache Issues
```bash
rm -rf ~/.cache/pre-commit
pre-commit clean
pre-commit install --install-hooks
```

### Permission Issues
```bash
chmod +x .git/hooks/pre-commit
```

### Python Version Issues
```bash
# Specify Python version
pre-commit run --all-files --python python3.11
```

## Advanced Usage

### Custom Hooks

Add to `.pre-commit-config.yaml`:
```yaml
- repo: local
  hooks:
    - id: pytest-check
      name: pytest-check
      entry: pytest
      language: system
      pass_filenames: false
      always_run: true
```

### Skip Specific Files

In `.pre-commit-config.yaml`:
```yaml
- id: black
  exclude: ^migrations/
```

## FAQ

**Q: Apakah pre-commit wajib?**
A: Sangat recommended! Ini memastikan code quality sebelum masuk ke repository.

**Q: Bisa disable pre-commit?**
A: Yes, dengan `git commit --no-verify`, tapi sangat tidak recommended.

**Q: Pre-commit memperlambat commit?**
A: Initial run mungkin lambat, tapi subsequent runs fast karena caching.

**Q: Bagaimana di CI/CD?**
A: Pre-commit sudah included di GitHub Actions, jadi akan run di pipeline juga.

---

**Setup Date**: 2026-01-18
**Pre-commit Version**: 3.6.0
**Status**: ✅ Ready to Use
