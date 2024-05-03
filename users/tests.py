from django.urls import reverse
from django.test import TestCase, Client
from users.models import User


class TestUserViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(phone_number='1234567890', password='12345')

    def test_register_view(self):
        response = self.client.get(reverse('users:register'))
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertContains(response, 'Register')
        print(response)

    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in')

    def test_profile_view(self):
        self.client.login(phone_number='1234567890', password='12345')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile')
