from django.contrib import admin

from content.models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'category', 'title', 'created_at', 'modified_at', 'paid_only')
    list_filter = ('author', 'category', 'title', 'created_at', 'paid_only')
