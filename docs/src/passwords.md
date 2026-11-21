# Updating Passwords

Currently we don't have a good "forgot my password" method on Pinry since that
generally requires an email to be sent. The current method for changing
passwords involves:

- Create a new super user `uv run python manage.py createsuperuser`
- Login to your admin panel `{your_website_url}/admin/`
- Go to the users section, select the user, change their password.

## Inside Docker

Run the command inside the container, which already uses the Docker
settings:

    docker compose exec pinry python manage.py createsuperuser

To reset a password directly:

    docker compose exec pinry python manage.py changepassword <username>
