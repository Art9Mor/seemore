from django.core.management import BaseCommand
from content.models import Author, Content
from users.models import User


class Command(BaseCommand):
    """
    Custom command for creating Alpha user and free content.
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

        author, created = Author.objects.get_or_create(user=user, defaults={'nickname': user.full_name})

        content_data = {
            'author': author,
            'title': 'Test content 1',
            'category': 'Free content',
            'content': 'This is a free content created for Alpha User.',
            'paid_only': False,
            'is_active': True,
        }
        content = Content.objects.create(**content_data)

        self.stdout.write(self.style.SUCCESS('Successfully created alpha user and free content.'))


