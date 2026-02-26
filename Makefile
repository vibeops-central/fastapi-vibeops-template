.PHONY: install dev lint format typecheck test test-bdd test-cov vibecheck

install:
	uv sync

dev:
	uv run uvicorn src.main:app --reload --port 8000

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src/

test:
	uv run pytest

test-bdd:
	uv run pytest tests/bdd/

test-cov:
	uv run pytest --cov=src --cov-report=term-missing

vibecheck:
	uv run vibecheck .
