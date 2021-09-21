"""Socials models admin."""

# Django
from django.contrib import admin
from django.apps import apps

# Models
from mydea.socials.models import Request, Connection


class RequestAdmin(admin.ModelAdmin):
    """Request model admin."""

    model = Request
    list_display = (        
        'get_sender_username', 
        'get_receiver_username', 
        'status'
    )

    def get_sender_username(self, obj):
        return obj.sender.username
    get_sender_username.admin_order_field = 'user'
    get_sender_username.short_description = 'Sender'

    def get_receiver_username(self, obj):
        return obj.receiver.username
    get_receiver_username.admin_order_field = 'user'
    get_receiver_username.short_description = 'Receiver'

    list_filter = ('status',)
    search_fields = (
        'sender__username',
        'receiver__username'
    )  

admin.site.register(Request, RequestAdmin)


class ConnectionAdmin(admin.ModelAdmin):
    """Connection model admin."""

    model = Connection
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

admin.site.register(Connection, ConnectionAdmin)
