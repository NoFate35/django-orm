MANAGE := poetry run python manage.py

test:
	poetry run python3 manage.py test django_orm.quote

server:
	poetry run manage.py runserver

makemigrations:
	@$(MANAGE) makemigrations 

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --print-sql