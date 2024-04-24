from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, timedelta

from .models import User, PaymentSubscription


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(phone_number='1234567890', email='test@example.com')
        self.subscription = PaymentSubscription.objects.create(
            user=self.user,
            amount=100,
            date=datetime.now(),
            expiration_date=datetime.now() + timedelta(days=30),
            payment_url='test_payment_url',
            is_active=True,
            subscription_period='short'
        )

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)

    def test_subscription_creation(self):
        self.assertEqual(PaymentSubscription.objects.count(), 1)

    def test_subscription_expiration(self):
        self.assertTrue(self.subscription.expiration_date > datetime.now())

    def test_register_view(self):
        client = Client()
        response = client.post(reverse('users:register'), {'phone_number': '9876543210', 'password1': 'testpass', 'password2': 'testpass'})
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        client = Client()
        client.force_login(self.user)
        response = client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)