.PHONY: help dev stop clean test test-backend test-frontend test-e2e seed logs lint format build deploy

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Flowto - Available Commands$(NC)"
	@echo "$(BLUE)================================$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

#################################################################
# Development
#################################################################

dev: ## Start all services (backend + frontend + databases)
	@echo "$(BLUE)Starting Flowto...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Services started!$(NC)"
	@echo "  Backend:  http://localhost:8000"
	@echo "  Frontend: http://localhost:3000"
	@echo "  API Docs: http://localhost:8000/docs"

stop: ## Stop all services
	@echo "$(YELLOW)Stopping services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Services stopped$(NC)"

restart: ## Restart all services
	@make stop
	@make dev

logs: ## Show logs from all services
	docker-compose logs -f --tail=100

logs-backend: ## Show backend logs only
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs only
	docker-compose logs -f frontend

clean: ## Stop services and clean volumes (⚠️  WARNING: deletes data!)
	@echo "$(RED)WARNING: This will delete all data!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		echo "$(GREEN)✓ Cleaned$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled$(NC)"; \
	fi

#################################################################
# Testing
#################################################################

test: test-backend test-frontend ## Run all tests (backend + frontend)

test-backend: ## Run backend tests with coverage
	@echo "$(BLUE)Running backend tests...$(NC)"
	docker-compose exec backend pytest tests/ -v --cov=app --cov-report=term-missing
	@echo "$(GREEN)✓ Backend tests completed$(NC)"

test-backend-fast: ## Run backend tests without coverage (faster)
	@echo "$(BLUE)Running backend tests (fast mode)...$(NC)"
	docker-compose exec backend pytest tests/ -v --no-cov
	@echo "$(GREEN)✓ Backend tests completed$(NC)"

test-frontend: ## Run frontend E2E tests
	@echo "$(BLUE)Running frontend E2E tests...$(NC)"
	cd frontend && npm run test:e2e
	@echo "$(GREEN)✓ Frontend tests completed$(NC)"

test-e2e: ## Run E2E tests with Playwright
	@echo "$(BLUE)Running E2E tests...$(NC)"
	cd frontend && npx playwright test
	@echo "$(GREEN)✓ E2E tests completed$(NC)"

test-coverage: ## Generate coverage report
	@echo "$(BLUE)Generating coverage report...$(NC)"
	docker-compose exec backend pytest tests/ --cov=app --cov-report=html
	@echo "$(GREEN)✓ Coverage report generated at backend/htmlcov/index.html$(NC)"

#################################################################
# Database
#################################################################

db-migrate: ## Run database migrations
	@echo "$(BLUE)Running migrations...$(NC)"
	docker-compose exec backend alembic upgrade head
	@echo "$(GREEN)✓ Migrations completed$(NC)"

db-rollback: ## Rollback last migration
	@echo "$(YELLOW)Rolling back last migration...$(NC)"
	docker-compose exec backend alembic downgrade -1
	@echo "$(GREEN)✓ Rollback completed$(NC)"

db-reset: ## Reset database (⚠️  WARNING: deletes all data!)
	@echo "$(RED)WARNING: This will reset the database!$(NC)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose exec backend alembic downgrade base; \
		docker-compose exec backend alembic upgrade head; \
		echo "$(GREEN)✓ Database reset$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled$(NC)"; \
	fi

seed: ## Seed database with demo data
	@echo "$(BLUE)Seeding database...$(NC)"
	docker-compose exec backend python scripts/seed_data.py
	@echo "$(GREEN)✓ Database seeded$(NC)"
	@echo "$(YELLOW)Demo credentials:$(NC)"
	@echo "  Email: demo@flowto.fr"
	@echo "  Password: Demo123!"

#################################################################
# Code Quality
#################################################################

lint: ## Run linters (backend + frontend)
	@echo "$(BLUE)Running linters...$(NC)"
	@make lint-backend
	@make lint-frontend
	@echo "$(GREEN)✓ Linting completed$(NC)"

lint-backend: ## Run backend linters (ruff, black, mypy)
	@echo "$(BLUE)Linting backend...$(NC)"
	docker-compose exec backend ruff check app/ tests/
	docker-compose exec backend black --check app/ tests/
	docker-compose exec backend mypy app/ --ignore-missing-imports

lint-frontend: ## Run frontend linters (eslint, prettier)
	@echo "$(BLUE)Linting frontend...$(NC)"
	cd frontend && npm run lint
	cd frontend && npx prettier --check "src/**/*.{ts,tsx,js,jsx,json,css}"

format: ## Format code (backend + frontend)
	@echo "$(BLUE)Formatting code...$(NC)"
	docker-compose exec backend black app/ tests/
	docker-compose exec backend ruff check --fix app/ tests/
	cd frontend && npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,css}"
	@echo "$(GREEN)✓ Code formatted$(NC)"

#################################################################
# Build & Deploy
#################################################################

build: ## Build Docker images
	@echo "$(BLUE)Building images...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ Build completed$(NC)"

build-no-cache: ## Build Docker images without cache
	@echo "$(BLUE)Building images (no cache)...$(NC)"
	docker-compose build --no-cache
	@echo "$(GREEN)✓ Build completed$(NC)"

ps: ## Show running services
	docker-compose ps

shell-backend: ## Open shell in backend container
	docker-compose exec backend /bin/bash

shell-frontend: ## Open shell in frontend container
	docker-compose exec frontend /bin/sh

shell-db: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U financeai -d financeai

#################################################################
# Utilities
#################################################################

install: ## Install all dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

update: ## Update dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	cd backend && pip install --upgrade -r requirements.txt
	cd frontend && npm update
	@echo "$(GREEN)✓ Dependencies updated$(NC)"

check: ## Run all checks (lint + test)
	@make lint
	@make test

ci: ## Run CI pipeline locally (lint + test + build)
	@echo "$(BLUE)Running CI pipeline...$(NC)"
	@make lint
	@make test
	@make build
	@echo "$(GREEN)✓ CI pipeline completed$(NC)"

health: ## Check services health
	@echo "$(BLUE)Checking services health...$(NC)"
	@echo -n "Backend:  "
	@curl -sf http://localhost:8000/health > /dev/null && echo "$(GREEN)✓ Healthy$(NC)" || echo "$(RED)✗ Down$(NC)"
	@echo -n "Frontend: "
	@curl -sf http://localhost:3000 > /dev/null && echo "$(GREEN)✓ Healthy$(NC)" || echo "$(RED)✗ Down$(NC)"
	@echo -n "Database: "
	@docker-compose exec postgres pg_isready -U financeai > /dev/null && echo "$(GREEN)✓ Healthy$(NC)" || echo "$(RED)✗ Down$(NC)"
	@echo -n "Redis:    "
	@docker-compose exec redis redis-cli ping > /dev/null && echo "$(GREEN)✓ Healthy$(NC)" || echo "$(RED)✗ Down$(NC)"

stats: ## Show Docker stats
	docker stats --no-stream

#################################################################
# Documentation
#################################################################

docs: ## Generate API documentation
	@echo "$(BLUE)API docs available at:$(NC)"
	@echo "  http://localhost:8000/docs (Swagger)"
	@echo "  http://localhost:8000/redoc (ReDoc)"

#################################################################
# Default
#################################################################

.DEFAULT_GOAL := help

