"""User graphql types"""

# Graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

# Models
from mydea.users.models import User, Profile


# User types
class CustomUserNode(DjangoObjectType):
    class Meta:
        model = User
        exclude = [
            'password',
            'last_login',
            'is_superuser',
            'is_staff',
            'is_active',
            'date_joined',
            'sender',
            'receiver'
        ]
        filter_fields = {
            'username': ['exact', 'icontains']
        }
        interfaces = (relay.Node, )

# Profile types
class ProfileNode(DjangoObjectType):
    class Meta:
        model = Profile
        exclude = ['post_set']
        filter_fields = []
        interfaces = (relay.Node, )
