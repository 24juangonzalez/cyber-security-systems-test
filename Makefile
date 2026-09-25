.PHONY: setup ui hooks test lint format format-check check clean

setup:
	uv sync

ui:
	uv run --locked --extra ui streamlit run streamlit_app.py --server.address 127.0.0.1

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
