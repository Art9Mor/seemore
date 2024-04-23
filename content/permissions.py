from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from users.models import User


@receiver(post_migrate)
def create_permissions(sender, **kwargs):
    content_type = ContentType.objects.get_for_model(User)
    permission, _ = Permission.objects.get_or_create(
        codename='add_content',
        name='Can add content',
        content_type=content_type,
    )
