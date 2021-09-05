"""Post models admin."""

# Django
from django.contrib import admin
from django.apps import apps

# Models
from mydea.socials.models import Request


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

admin.site.register(Request, RequestAdmin)