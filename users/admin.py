from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'is_author', 'is_subscribed', 'is_active')
    search_fields = ('full_name', 'phone_number', 'email')
    list_filter = ('is_author', 'is_subscribed', 'is_active')
