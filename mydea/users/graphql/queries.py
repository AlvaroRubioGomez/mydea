"""User graphql queries"""

# Graphene
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay

# Django-graphql-auth
from graphql_jwt.decorators import login_required

# Types
from .types import CustomUserNode


# User queries
class UsersQuery(graphene.ObjectType): 
    find_users = DjangoFilterConnectionField(CustomUserNode) 