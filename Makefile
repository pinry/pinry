dev-docker-serve:
	docker compose -f docker-compose.dev.yml up --build
docker-build:
	docker build -f Dockerfile.autobuild -t pinry:local .
docker-smoke-test: docker-build
	./docker/tests/smoke.sh pinry:local
backup-images:
	uv run python manage.py dumpdata django_images > db-backup.django_images.json
backup-all:
	uv run python manage.py dumpdata > db-backup.all.json
migrate:
	uv run python manage.py migrate
migrate-no-input:
	uv run python manage.py migrate --noinput
makemigrations:
	uv run python manage.py makemigrations
recover-all:
	uv run python manage.py loaddata db-backup.all.json
collect-static-no-input:
	uv run python manage.py collectstatic --noinput
bootstrap:
	make install
	make collect-static-no-input
serve-gunicorn:
	uv run gunicorn pinry.wsgi -b 0.0.0.0:8000 -w 4 --capture-output --timeout 30 --user www-data --group www-data
serve:
	uv run python manage.py runserver 0.0.0.0:8000
lock:
	uv lock
install:
	uv sync
test:
	uv run python manage.py test
shell:
	uv run python manage.py shell
flake8:
	uv run flake8
docs-serve:
	uv run mkdocs serve
docs-build:
	uv run mkdocs build
docs-publish:
	uv run mkdocs gh-deploy
