# Updating Passwords

Currently we don't have a good "forgot my password" method on Pinry since that
generally requries an email to be sent. The current method for changing
passwords involves:

- Create a new super user `pipenv run python manage.py createsuperuser`
- Login to your admin panel `{your_website_url}/admin/`
- Go to the users section, select the user, change their password.
