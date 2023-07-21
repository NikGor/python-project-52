.PHONY: install test lint run clean

install:
	poetry install

test:
	poetry run python manage.py test

lint:
	poetry run flake8

run:
	poetry run python manage.py runserver

clean:
	find . -name "*.pyc" -delete

add-and-commit:
	git add .
	git commit --amend --no-edit
	git push --force

build:
	docker build -t django-app .


