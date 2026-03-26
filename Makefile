install-dev:
	@echo "Installing local package..."
	uv sync
	uv run prek install
test:
	@echo "Running tests..."
	uv run prek run --all-files
	uv run mypy .
	# Follow the test practices recommanded by LangChain (v0.3)
	# See https://python.langchain.com/docs/contributing/how_to/integrations/standard_tests/
	uv run pytest --cov=src/langchain_linkup/ --cov-report term-missing --disable-socket --allow-unix-socket tests/unit_tests
	uv run pytest tests/integration_tests

update-dependencies:
	uv lock --upgrade
update-pre-commit-hooks:
	uv run prek autoupdate --cooldown-days 14
