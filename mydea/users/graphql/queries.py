"""User graphql queries"""

# Graphene
from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField

# Types
from .types import UserNode

class UserQuery(ObjectType):
    """User queries for retrieving one or all users"""
    user = relay.Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)
