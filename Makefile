.PHONY: run
run:
	python3 manage.py runserver

.PHONY: makemigrations
makemigrations:
	python3 manage.py makemigrations

.PHONY: migrate
migrate:
	python3 manage.py migrate

.PHONY: test
test:
	python3 manage.py test

.PHONY: shell
shell:
	python3 manage.py shell

.PHONY: check
check:
	python3 manage.py check

.PHONY: createsuperuser
createsuperuser:
	python3 manage.py createsuperuser

.PHONY: collectstatic
collectstatic:
	python3 manage.py collectstatic

.PHONY: makemessages
makemessages:
	django-admin makemessages -l ru

.PHONY: compilemessages
compilemessages:
	django-admin compilemessages

build:
	docker build -t your-image-name .

run:
	docker run -p 8000:8000 your-image-name
