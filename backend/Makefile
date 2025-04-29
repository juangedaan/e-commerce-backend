# Makefile

# Development commands
build-dev:
	docker-compose build

up-dev:
	docker-compose up

down-dev:
	docker-compose down

# Production commands
build-prod:
	docker-compose -f docker-compose.production.yml build

up-prod:
	docker-compose -f docker-compose.production.yml up

down-prod:
	docker-compose -f docker-compose.production.yml down

# Database migration helper (example if you later add Alembic)
migrate:
	docker-compose exec backend alembic upgrade head

# Clean up Docker artifacts
prune:
	docker system prune -af
	docker volume prune -f

# Run full test suite with clean output and durations
test:
	pytest --tb=short --durations=5 -q backend/tests

# Run tests and generate HTML report
test-html:
	pytest --html=report.html --self-contained-html backend/tests

