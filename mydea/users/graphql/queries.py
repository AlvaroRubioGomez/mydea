"""User graphql queries"""

# Graphene
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay

# Types
from .types import CustomUserNode

# Models
from mydea.posts.models import Post


# User queries
class UsersQuery(graphene.ObjectType): 
    users = DjangoFilterConnectionField(CustomUserNode)  