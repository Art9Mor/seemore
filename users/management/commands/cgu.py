from django.core.management import BaseCommand
from content.models import Author, Content
from users.models import User


class Command(BaseCommand):
    """
    Custom command for creating Gamma user and free content.
    """

    def handle(self, *args, **options):
        user = User.objects.create(
            phone_number='+1-111-111-11-11',
            email='gamma@symple.mail',
            full_name='Alpha User',
            is_active=True,
        )
        user.set_password('8756')
        user.save()

        self.stdout.write(self.style.SUCCESS('Successfully created gamma user.'))
