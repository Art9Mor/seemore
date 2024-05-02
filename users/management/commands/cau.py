import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Custom command for creating alpha user.
    """
    def handle(self, *args, **options):
        user = User.objects.create(
            phone_number='+1-123-456-78-90',
            email='alpha@symple.mail',
            full_name='Alpha User',
            is_author=True,
            is_active=True,
        )
        user.set_password('1234')
        user.save()
