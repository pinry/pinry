backup-images:
	pipenv run python manage.py dumpdata django_images > db-backup.django_images.json
backup-all:
	pipenv run python manage.py dumpdata > db-backup.all.json
migrate:
	pipenv run python manage.py migrate
recover-all:
	pipenv run python manage.py loaddata db-backup.all.json
serve:
	pipenv run python manage.py runserver 0.0.0.0:8000
install:
	pipenv install
test:
	pipenv run python manage.py test
