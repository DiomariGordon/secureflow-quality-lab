.PHONY: install browsers run test test-fast test-api test-security test-e2e coverage crypto-report clean

install:
	python -m pip install -e ".[dev]"

browsers:
	python -m playwright install chromium

run:
	python -m uvicorn secureflow.app:app --reload --host 127.0.0.1 --port 8000

test:
	python -m pytest -vv

test-fast:
	python -m pytest -m "not e2e" --cov=secureflow --cov-report=term-missing

test-api:
	python -m pytest tests/api/test_api_workflow.py tests/api/test_data_integrity.py -vv

test-security:
	python -m pytest -m security -vv

test-e2e:
	python -m pytest -m e2e -vv

coverage:
	python -m pytest -m "not e2e" --cov=secureflow --cov-report=term-missing --cov-report=html

crypto-report:
	secureflow-crypto-inventory config/crypto_inventory.json --format markdown --output reports/crypto-readiness.md

clean:
	rm -rf .pytest_cache htmlcov test-results playwright-report secureflow.db reports/*.json reports/*.xml reports/*.txt
