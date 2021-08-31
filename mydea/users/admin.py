"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from mydea.users.models import User


class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_verified')
    list_filter = ('created', 'modified')


admin.site.register(User, CustomUserAdmin)
