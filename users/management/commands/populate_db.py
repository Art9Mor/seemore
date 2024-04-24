from django.core.management.base import BaseCommand
import random
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone
from content.models import Author, Content, Report
from users.models import PaymentSubscription

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        self.create_users()
        self.create_authors()
        self.create_content()
        self.create_reports()

    def create_users(self, num_users=10):
        for _ in range(num_users):
            phone_number = f'+7900{random.randint(1000000, 9999999)}'
            email = f'user{random.randint(1000, 9999)}@example.com'
            user = User.objects.create_user(phone_number=phone_number, email=email, password='password123')
            if random.choice([True, False]):
                PaymentSubscription.objects.create(
                    user=user,
                    amount=random.randint(10, 100),
                    date=timezone.now() - timedelta(days=random.randint(1, 365)),
                    subscription_period=random.choice(['short', 'long', 'ultra'])
                )

    def create_authors(self):
        users = User.objects.all()
        for user in users:
            if random.choice([True, False]):
                Author.objects.create(user=user)

    def create_content(self, num_content=20):
        authors = Author.objects.all()
        for _ in range(num_content):
            author = random.choice(authors)
            Content.objects.create(
                author=author,
                category=random.choice(['Technology', 'Science', 'Art', 'Food', 'Travel']),
                title=f'Test Title {_}',
                content=f'This is a test content {_}.',
                created_at=timezone.now() - timedelta(days=random.randint(1, 365)),
                paid_only=random.choice([True, False]),
                is_active=random.choice([True, False]),
                views_count=random.randint(0, 1000)
            )

    def create_reports(self, num_reports=30):
        contents = Content.objects.all()
        users = User.objects.all()
        for _ in range(num_reports):
            content = random.choice(contents)
            user = random.choice(users)
            Report.objects.create(
                content=content,
                user=user,
                title=f'Test Report {_}',
                comment=f'This is a test report {_}.',
                created_at=timezone.now() - timedelta(days=random.randint(1, 365))
            )
