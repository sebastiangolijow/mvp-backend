.PHONY: local
local:
	docker-compose up

.PHONY: local
local-build:
	docker-compose build

.PHONY: test-all
test-all:
	docker-compose run --rm app sh -c "python manage.py test"