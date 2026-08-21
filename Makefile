.PHONY: backend agent test-backend test-agent test clean help

backend:
	docker compose up --build

agent:
	cd agent_framework && uv run python main.py

test-backend:
	cd backend/chatverse && ./mvnw test

test-agent:
	cd agent_framework && uv run pytest

test: test-backend test-agent

clean:
	docker compose down -v

help:
	@echo "  make backend       - Start backend + PostgreSQL (docker)"
	@echo "  make agent         - Run agent framework"
	@echo "  make test-backend  - Run Java tests"
	@echo "  make test-agent    - Run Python tests"
	@echo "  make test          - Run all tests"
	@echo "  make clean         - Stop containers + remove data"
