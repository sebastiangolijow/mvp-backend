.PHONY: local
local:
	docker-compose up

.PHONY: local
local-build:
	docker-compose build ${ARGS}

.PHONY: test-all
test-all:
	docker-compose run --rm app sh -c "python manage.py test"

.PHONY: local-build-clean
local-build-clean: ## Builds docker images of the dev environment with no cache
	ARGS=--no-cache make local-build

.PHONY: makemigrations
makemigrations:
	docker-compose run --rm app sh -c "python manage.py makemigrations"

.PHONY: migrate
migrate:
	docker-compose run --rm app sh -c "python manage.py migrate"