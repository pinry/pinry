backup-images:
	pipenv run python manage.py dumpdata django_images > db-backup.django_images.json
backup-all:
	pipenv run python manage.py dumpdata > db-backup.all.json
migrate:
	pipenv run python manage.py migrate
makemigrations:
	pipenv run python manage.py makemigrations
recover-all:
	pipenv run python manage.py loaddata db-backup.all.json
bootstrap:
	make install
	pipenv run python manage.py collectstatic
serve:
	pipenv run python manage.py runserver 0.0.0.0:8000
install:
	pipenv install
test:
	pipenv run python manage.py test
shell:
	pipenv run python manage.py shell
flake8:
	pipenv run flake8
