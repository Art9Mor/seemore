from django.contrib import admin

from content.models import Content, Author, Report


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'category', 'title', 'created_at', 'modified_at', 'paid_only')
    list_filter = ('author', 'category', 'title', 'created_at', 'paid_only')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'nickname', 'exists_since', 'article_count')
    list_filter = ('nickname', 'exists_since', 'article_count')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'user', 'slug', 'title', 'created_at')
    list_filter = ('id', 'slug', 'title', 'created_at')
