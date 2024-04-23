from django.contrib.auth.models import Permission
from django.db import models
from django.db.models import Count

from users.models import User

NULLABLE = {
    'blank': True,
    'null': True,
}


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, verbose_name='User')
    exists_since = models.DateField(auto_now_add=True, verbose_name='Exists since')
    article_count = models.PositiveIntegerField(default=0, verbose_name='Article Count')

    def __str__(self):
        return f'Author: {self.user.full_name}'

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Content(models.Model):
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, verbose_name='Author')
    category = models.CharField(max_length=150, verbose_name='Category', default='Unknown')
    title = models.CharField(max_length=255, verbose_name='Title')
    content = models.TextField(verbose_name='Content', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modified', **NULLABLE)
    image = models.ImageField(upload_to='content/', **NULLABLE)
    paid_only = models.BooleanField(default=False, verbose_name='Paid only')
    is_active = models.BooleanField(default=True, verbose_name='Is published')
    views_count = models.IntegerField(default=0, verbose_name='Views')

    def __str__(self):
        return f'Article: {self.category}/{self.title}'

    class Meta:
        verbose_name = 'Content'
        verbose_name_plural = 'Contents'
        ordering = ['category', 'title']


class Report(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name='Content to report')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Reporting user', null=True)
    comment = models.TextField(verbose_name='Comment', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date of reporting')

    def check_and_deactivate_content(cls):
        """
        Checks the number of complaints about the content and deactivates it if the number of complaints exceeds 5.
        """
        content_with_reports = Content.objects.annotate(num_reports=Count('report'))
        for content in content_with_reports:
            if content.num_reports >= 5:
                content.is_active = False
                content.save()

    def __str__(self):
        return f'Report from {self.user.full_name}'

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        unique_together = (('content', 'user'),)
