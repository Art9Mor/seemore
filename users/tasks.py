from celery import shared_task
from datetime import datetime, timedelta

from django.utils import timezone

from .models import PaymentSubscription, User


@shared_task
def check_subscription_expiry():
    """
    Checks subscription expiry. Deactivating an expired subscription.
    """
    subscriptions = PaymentSubscription.objects.filter(is_active=True, expiration_date__lte=datetime.now())
    for subscription in subscriptions:
        subscription.is_active = False
        subscription.save()


@shared_task
def delete_inactive_users():
    three_weeks_ago = timezone.now() - timedelta(weeks=3)
    inactive_users = User.objects.filter(is_active=False, date_deactivated__lte=three_weeks_ago)
    inactive_users.delete()
