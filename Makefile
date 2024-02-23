.PHONY: local
local:
	docker-compose up

.PHONY: local
local-build:
	docker-compose build ${ARGS}

.PHONY: test-all
test-all:
	docker-compose run --rm app sh -c "python manage.py test"

local-build-clean: ## Builds docker images of the dev environment with no cache
	ARGS=--no-cache make local-build