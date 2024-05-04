from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone

from content.models import Author
from users.models import User, PaymentSubscription


class Command(BaseCommand):
    """
    Custom command for creating Omega user and subscription.
    """

    def handle(self, *args, **options):
        user = User.objects.create(
            phone_number='+0-987-654-32-11',
            email='omega@symple.mail',
            full_name='Omega User',
            is_subscribed=True,
            is_active=True,
        )
        user.set_password('4321')
        user.save()

        subscription_data = {
            'user': user,
            'date': timezone.now(),
            'payment_url': '345',
            'amount': 2100,
            'is_active': True,
            'subscription_period': 'ultra',
        }
        subscription = PaymentSubscription.objects.create(**subscription_data)

        self.stdout.write(self.style.SUCCESS('Successfully created omega user with subscription.'))
