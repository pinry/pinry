# Updating Passwords

Currently we don't have a good "forgot my password" method on Pinry since that
generally requires an email to be sent. The current method for changing
passwords involves:

- Create a new super user `pipenv run python manage.py createsuperuser`
- Login to your admin panel `{your_website_url}/admin/`
- Go to the users section, select the user, change their password.

Note: If you use that command to create superuser **inside docker**, please add `--settings=pinry.settings.docker`
to command like, just like `python manage.py createsuperuser --settings=pinry.settings.docker`
