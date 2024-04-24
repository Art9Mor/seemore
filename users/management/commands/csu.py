from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Custom command for creating superuser
    """
    def handle(self, *args, **options):
        user = User.objects.create(
            phone_number='+7666666666',
            email='online_school@yandex.ru',
            full_name='Amadey Mozart',
            is_author=True,
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        user.set_password('666')
        user.save()
