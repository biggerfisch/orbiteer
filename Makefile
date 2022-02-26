all: lint test

test:
	@./scripts/test.sh

lint:
	@./scripts/lint.sh

format:
	@./scripts/format.sh

.PHONY: all test lint format
