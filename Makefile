MANAGE := poetry run python manage.py

test:
	poetry run python3 manage.py test

server:
	poetry run manage.py runserver

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --print-sql