from django.contrib.auth.models import Permission
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from users.models import User

NULLABLE = {
    'blank': True,
    'null': True,
}


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, verbose_name='User')
    exists_since = models.DateField(auto_now_add=True, verbose_name='Exists since')
    article_count = models.PositiveIntegerField(default=0, verbose_name='Article count')
    nickname = models.CharField(max_length=255, verbose_name='Nickname', blank=True)

    def save(self, *args, **kwargs):
        self.nickname = self.user.full_name
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Author: {self.nickname}'

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Content(models.Model):
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, verbose_name='Author')
    category = models.CharField(max_length=150, verbose_name='Category', default='Unknown')
    slug = models.CharField(max_length=100, verbose_name='Slug', **NULLABLE)
    title = models.CharField(max_length=255, verbose_name='Title')
    content = models.TextField(verbose_name='Content', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modified', **NULLABLE)
    image = models.ImageField(upload_to='content/', **NULLABLE)
    video_url = models.URLField(max_length=200, verbose_name='Video URL', **NULLABLE)
    paid_only = models.BooleanField(default=False, verbose_name='Paid only')
    is_active = models.BooleanField(default=True, verbose_name='Is published')
    views_count = models.IntegerField(default=0, verbose_name='Views')
    num_reports = models.IntegerField(default=0, verbose_name='Reports')

    def __str__(self):
        return f'Article: {self.category}/{self.title}'

    class Meta:
        verbose_name = 'Content'
        verbose_name_plural = 'Contents'
        ordering = ['category', 'title']


class Report(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name='Content to report')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Reporting user', null=True)
    slug = models.CharField(max_length=100, verbose_name='Slug', **NULLABLE)
    title = models.CharField(max_length=255, verbose_name='Title')
    comment = models.TextField(verbose_name='Comment', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date of reporting')
    screenshots = models.ImageField(upload_to='screenshots/', verbose_name='Screenshots', **NULLABLE)

    @classmethod
    def check_and_deactivate_content(cls):
        """
        Checks the number of complaints about the content and deactivates it if the number of complaints exceeds 5.
        """
        for content in Content.objects.all():
            num_reports = Report.objects.filter(content=content).count()
            if num_reports >= 5:
                content.is_active = False
                content.save()

    def __str__(self):
        return f'Report for Article: {self.content.category}/{self.content.title}/{self.content.author.nickname}'

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'


@receiver(post_save, sender=Report)
@receiver(post_delete, sender=Report)
def update_content_activity(sender, instance, **kwargs):
    Report.check_and_deactivate_content()
