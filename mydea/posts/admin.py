"""Post models admin."""

# Django
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.apps import apps

# Models
from mydea.posts.models import Post


class PostAdmin(admin.ModelAdmin):
    """Post model admin."""

    model = Post
    list_display = (        
        'get_username', 
        'body', 
        'visibility', 
        'modified'
    )

    def get_username(self, obj):
        return obj.created_by.user.username
    get_username.admin_order_field = 'user'
    get_username.short_description = 'Username'

    search_fields = (
        'profile__user__username', 
        'profile__user__email')
    list_filter = ('visibility',)

admin.site.register(Post, PostAdmin)