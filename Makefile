all: setup lint test

setup:
	@./scripts/setup.sh

test:
	@./scripts/test.sh

lint:
	@./scripts/lint.sh

format:
	@./scripts/format.sh

.PHONY: all setup test lint format
