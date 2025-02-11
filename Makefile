install:
	uv sync
run:
	uv run gendiff
build:
	uv build
package-install:
	uv tool install dist/*.whl
package-reinstall:
	uv tool install --reinstall dist/*.whl
lint:
	uv run ruff check
test:
	uv run pytest
test-coverage:
	uv run pytest --cov=gendiff --cov-report xml tests/
