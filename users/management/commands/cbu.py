from django.core.management import BaseCommand
from django.utils import timezone

from content.models import Author, Content
from users.models import User, PaymentSubscription


class Command(BaseCommand):
    """
    Custom command for creating Brutal user and content.
    """

    def handle(self, *args, **options):
        user = User.objects.create(
            phone_number='+6-666-666-66-13',
            email='brutal@symple.mail',
            full_name='Alpha User',
            is_author=True,
            is_subscribed=True,
            is_active=True,
        )
        user.set_password('0987')
        user.save()

        author, created = Author.objects.get_or_create(user=user, defaults={'nickname': user.full_name})

        subscription_data = {
            'user': user,
            'date': timezone.now(),
            'payment_url': '',
            'is_active': True,
            'subscription_period': 'ultra',
        }
        subscription = PaymentSubscription.objects.create(**subscription_data)

        content_data_free = {
            'author': author,
            'title': 'Test content 2',
            'category': 'Free content',
            'content': 'This is a free content created for Brutal User.',
            'is_active': True,
        }
        content = Content.objects.create(**content_data_free)

        content_data_paid = {
            'author': author,
            'title': 'Test content 3',
            'category': 'Paid content',
            'content': 'This is a paid content created for Brutal User.',
            'paid_only': True,
            'is_active': True,
        }
        content = Content.objects.create(**content_data_paid)

        self.stdout.write(self.style.SUCCESS('Successfully created brutal user, subscription and content.'))
