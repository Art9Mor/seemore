from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

NULLABLE = {
    'blank': True,
    'null': True,
}

phone_number_validator = RegexValidator(
    regex=r'^[\d\+\-]+$',
    message='Phone number can only contain digits, +, and - characters.'
)

SUBSCRIPTION_PERIOD = [
    ('short', 'Short'),
    ('long', 'Long'),
    ('ultra', 'Ultra'),
]


class User(AbstractUser):
    username = None

    full_name = models.CharField(max_length=255, verbose_name="Full Name", default='Noname')
    phone_number = models.CharField(max_length=20, unique=True, verbose_name='Phone Number', validators=[phone_number_validator])
    email = models.EmailField(unique=False, verbose_name='Email', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Avatar', **NULLABLE)
    is_author = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False, verbose_name="Subscription")

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class PaymentSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User')
    amount = models.IntegerField(verbose_name="Amount")
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date of subscription')
    expiration_date = models.DateTimeField(verbose_name='Expiration Date', **NULLABLE)
    payment_url = models.TextField(unique=True, verbose_name='Payment session', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Activity of subscription')
    subscription_period = models.CharField(max_length=20, verbose_name='Subscription Period',
                                           choices=SUBSCRIPTION_PERIOD)

    def __str__(self):
        return f'Subscription for {self.user.full_name} from {self.date} is active'

    def save(self, *args, **kwargs):
        if not self.expiration_date:
            if self.subscription_period == 'short':
                self.expiration_date = self.date + timedelta(days=30)  # 30 days subscription
            elif self.subscription_period == 'long':
                self.expiration_date = self.date + timedelta(days=180)  # 6 month subscription
            elif self.subscription_period == 'ultra':
                self.expiration_date = self.date + timedelta(days=365)  # 1 year subscription
        super(PaymentSubscription, self).save(*args, **kwargs)
