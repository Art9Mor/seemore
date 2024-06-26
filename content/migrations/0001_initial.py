# Generated by Django 5.0.4 on 2024-05-03 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exists_since', models.DateField(auto_now_add=True, verbose_name='Exists since')),
                ('article_count', models.PositiveIntegerField(default=0, verbose_name='Article count')),
                ('nickname', models.CharField(blank=True, max_length=255, verbose_name='Nickname')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='Unknown', max_length=150, verbose_name='Category')),
                ('slug', models.CharField(blank=True, max_length=100, null=True, verbose_name='Slug')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('modified_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Modified')),
                ('image', models.ImageField(blank=True, null=True, upload_to='content/')),
                ('video_url', models.URLField(blank=True, null=True, verbose_name='Video URL')),
                ('paid_only', models.BooleanField(default=False, verbose_name='Paid only')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is published')),
                ('views_count', models.IntegerField(default=0, verbose_name='Views')),
                ('num_reports', models.IntegerField(default=0, verbose_name='Reports')),
            ],
            options={
                'verbose_name': 'Content',
                'verbose_name_plural': 'Contents',
                'ordering': ['category', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(blank=True, max_length=100, null=True, verbose_name='Slug')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date of reporting')),
                ('screenshots', models.ImageField(blank=True, null=True, upload_to='screenshots/', verbose_name='Screenshots')),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
            },
        ),
    ]
