.PHONY: test test-cov coverage-html lint fmt

test:
	PYTHONDONTWRITEBYTECODE=1 pytest

test-cov:
	PYTHONDONTWRITEBYTECODE=1 pytest

coverage-html:
	PYTHONDONTWRITEBYTECODE=1 pytest --cov-report=html
