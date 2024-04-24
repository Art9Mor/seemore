from django.test import TestCase, Client
from django.urls import reverse

from .models import Author, Content, Report
from users.models import User


class ContentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(user=self.user)
        self.content = Content.objects.create(
            author=self.author,
            category='Test Category',
            slug='test-article',
            title='Test Article',
            content='This is a test article.',
            image='test_image.jpg',
            video_url='https://example.com/test_video.mp4',
            paid_only=False,
            is_active=True,
            views_count=0
        )
        self.report = Report.objects.create(
            content=self.content,
            user=self.user,
            slug='test-report',
            title='Test Report',
            comment='This is a test report.',
            screenshots='test_screenshot.jpg'
        )

    def test_content_creation(self):
        self.assertEqual(Content.objects.count(), 1)

    def test_report_creation(self):
        self.assertEqual(Report.objects.count(), 1)

    def test_author_creation(self):
        self.assertEqual(Author.objects.count(), 1)

    def test_content_detail_view(self):
        client = Client()
        response = client.get(reverse('content:content_detail', kwargs={'pk': self.content.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.content.title)

    def test_report_detail_view(self):
        client = Client()
        response = client.get(reverse('content:report_detail', kwargs={'pk': self.report.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.report.title)

    def test_home_view(self):
        client = Client()
        response = client.get(reverse('content:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home Page')
