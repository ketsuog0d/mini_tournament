.PHONY: dev migrate test

dev:
	docker-compose up --build

migrate:
	docker-compose run --rm api alembic upgrade head

test:
	docker-compose run --rm api pytest
