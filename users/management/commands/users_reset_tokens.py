from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from rest_framework.authtoken.models import Token
        Token.objects.all().delete()
