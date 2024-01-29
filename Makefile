.PHONY: local
local:
	docker-compose up

.PHONY: test-all
test-all:
	docker-compose run --rm app sh -c "python manage.py test"