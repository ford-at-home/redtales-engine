.PHONY: help install dev-install test lint format clean run-cli run-web

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make dev-install   - Install development dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linting"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean cache and temporary files"
	@echo "  make run-cli       - Run CLI tool"
	@echo "  make run-web       - Run Streamlit web interface"

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ -v

lint:
	flake8 backend/ frontend/ tests/
	mypy backend/ frontend/

format:
	black backend/ frontend/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .coverage
	rm -rf output/stories/*.md output/stories/*.json

run-cli:
	python -m backend.cli

run-web:
	streamlit run frontend/app.py

# Development shortcuts
dev: dev-install
	@echo "Development environment ready!"

check: lint test
	@echo "All checks passed!"

# Reddit API test
test-reddit:
	python -c "from backend.reddit_scraper import test_connection; test_connection()"

# AI API test
test-ai:
	python -c "from backend.ai_client import test_connection; test_connection()"