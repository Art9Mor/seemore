from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from users.models import PaymentSubscription


def create_payment_subscription_permission(sender, **kwargs):
    """
    Creates permission to create payment subscription.
    """
    content_type = ContentType.objects.get_for_model(PaymentSubscription)
    Permission.objects.get_or_create(
        codename='add_paymentsubscription',
        name='Can add payment subscription',
        content_type=content_type,
    )


@receiver(post_migrate)
def post_migrate_handler(sender, **kwargs):
    create_payment_subscription_permission(sender)
