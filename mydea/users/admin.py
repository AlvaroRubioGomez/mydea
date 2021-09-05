"""User models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.apps import apps

# Models
from mydea.users.models import User, Profile

class CustomUserAdmin(UserAdmin):
    """User model admin."""

    list_display = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('created', 'modified')

admin.site.register(User, CustomUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    model = Profile
    list_display = [
        'get_username',
        'get_following',
        'get_followers',
    ]

    def get_username(self, obj):
        return obj.user.username
    get_username.admin_order_field = 'user'
    get_username.short_description = 'Username'

    def get_following(self, obj):        
        return list(obj.following.all())
    get_following.admin_order_field = 'user'
    get_following.short_description = 'Following'

    def get_followers(self, obj):        
        return list(obj.followers.all())
    get_followers.admin_order_field = 'user'
    get_followers.short_description = 'Followers'

    # search_fields = ('user__username', 'user__email')
    # list_filter = ('posts__visibility',)

admin.site.register(Profile, ProfileAdmin)


# graphl-auth
app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)


