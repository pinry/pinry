dev-docker-serve:
	docker-compose up web
dev-docker-build-frontend:
	docker-compose up build_frontend
backup-images:
	poetry run python manage.py dumpdata django_images > db-backup.django_images.json
backup-all:
	poetry run python manage.py dumpdata > db-backup.all.json
migrate:
	poetry run python manage.py migrate
migrate-no-input:
	poetry run python manage.py migrate --noinput
makemigrations:
	poetry run python manage.py makemigrations
recover-all:
	poetry run python manage.py loaddata db-backup.all.json
collect-static-no-input:
	poetry run python manage.py collectstatic --noinput
bootstrap:
	make install
	make collect-static-no-input
serve-gunicorn:
	poetry run gunicorn pinry.wsgi -b 0.0.0.0:8000 -w 4 --capture-output --timeout 30 --user www-data --group www-data
serve:
	poetry run python manage.py runserver 0.0.0.0:8000
export-requirements-dev:
	poetry export --dev -f requirements.txt -o requirements-dev.txt
export-requirements:
	poetry export -f requirements.txt -o requirements.txt
	make export-requirements-dev
install:
	poetry install
test:
	poetry run python manage.py test
test-in-ci:
	python manage.py test
shell:
	poetry run python manage.py shell
flake8:
	poetry run flake8
flake8-in-ci:
	flake8
docs-serve:
	poetry run mkdocs serve
docs-build:
	poetry run mkdocs build
docs-publish:
	poetry run mkdocs gh-deploy
