"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.apps import apps

# Models
from mydea.users.models import User

# custom user
class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_verified')
    list_filter = ('created', 'modified')

admin.site.register(User, CustomUserAdmin)

# graphl-auth
app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)


