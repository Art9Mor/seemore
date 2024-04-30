from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Content, Author, Report


class TestContentViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(phone_number='+79856783526', password='12345')
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
        self.client.force_login(self.user)

    def test_home_view(self):
        response = self.client.get(reverse('content:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Home Page')

    def test_content_list_view(self):
        response = self.client.get(reverse('content:content_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Content List')

    def test_content_detail_view(self):
        response = self.client.get(reverse('content:content_detail', kwargs={'pk': self.content.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.content.title)

    def test_content_update_view(self):
        response = self.client.get(reverse('content:content_update', kwargs={'pk': self.content.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.content.title)
        response = self.client.post(reverse('content:content_update', kwargs={'pk': self.content.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('content:home'))

    def test_content_update(self):
        new_title = 'Updated Test Article'
        new_content = 'This is an updated test article.'
        updated_data = {
            'title': new_title,
            'content': new_content,
        }
        response = self.client.post(reverse('content:content_update', kwargs={'pk': self.content.pk}), updated_data)
        self.assertEqual(response.status_code, 302)
        updated_content = Content.objects.get(pk=self.content.pk)
        self.assertEqual(updated_content.title, new_title)
        self.assertEqual(updated_content.content, new_content)
