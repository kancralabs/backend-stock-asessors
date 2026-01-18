.PHONY: help install dev test coverage lint format clean docker-up docker-down precommit

help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install dev dependencies"
	@echo "  make setup        - Install dev dependencies + pre-commit hooks"
	@echo "  make dev          - Run development server"
	@echo "  make test         - Run tests"
	@echo "  make coverage     - Run tests with coverage report"
	@echo "  make lint         - Run linting"
	@echo "  make format       - Format code with black"
	@echo "  make precommit    - Run pre-commit on all files"
	@echo "  make clean        - Clean cache and build files"
	@echo "  make docker-up    - Start Docker services"
	@echo "  make docker-down  - Stop Docker services"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

setup:
	pip install -r requirements-dev.txt
	pre-commit install
	@echo "✅ Setup complete! Pre-commit hooks installed."

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

coverage:
	pytest --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=80

lint:
	flake8 app/
	black --check app/

format:
	black app/
	isort app/

precommit:
	pre-commit run --all-files

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f api
