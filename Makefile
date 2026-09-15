.PHONY: setup test lint format check clean

setup:
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

check: lint test

clean:
	find . -path ./.git -prune -o -path ./.venv -prune -o \
		-type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .mypy_cache build dist
