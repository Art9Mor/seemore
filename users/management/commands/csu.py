import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Custom command for creating superuser
    """
    def handle(self, *args, **options):
        user = User.objects.create(
            phone_number=os.getenv('SUPERUSER_PHONE'),
            email='seemore@symple.mail',
            full_name='Amadey Mozart',
            is_author=True,
            is_subscribed=True,
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.save()
