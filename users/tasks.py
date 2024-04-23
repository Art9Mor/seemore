from celery import shared_task
from datetime import datetime
from .models import PaymentSubscription


@shared_task
def check_subscription_expiry():
    """
    Checks subscription expiry. Deactivating an expired subscription.
    """
    subscriptions = PaymentSubscription.objects.filter(is_active=True, expiration_date__lte=datetime.now())
    for subscription in subscriptions:
        subscription.is_active = False
        subscription.save()
