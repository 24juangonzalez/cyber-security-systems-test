.PHONY: help setup dev ui hooks test lint format format-check check clean

help:
	@printf '%s\n' \
		'make dev    Start the app through the beginner launcher' \
		'make ui     Alias for make dev' \
		'make check  Run lint, formatting checks, and tests' \
		'make setup  Install project dependencies' \
		'make hooks  Enable checks before pushing'

setup:
	uv sync

dev:
	uv run --locked --extra ui python development.py

ui: dev

hooks:
	git config --local core.hooksPath .githooks

test:
	uv run --extra ui pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

format-check:
	uv run ruff format --check .

check: lint format-check test

clean:
	find . -path ./.git -prune -o -path ./.venv -prune -o \
		-type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .mypy_cache build dist
