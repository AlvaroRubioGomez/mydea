"""Post graphql types"""

# Graphene
import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

# Models
from mydea.posts.models import Post

# Django-raphql-auth
from graphql_auth.schema import UserNode

# Node types
class PostNode(DjangoObjectType):
    created_by = graphene.Field(UserNode)

    class Meta:
        model = Post

        filter_fields = ['created_by__username']
        interfaces = (relay.Node, )     





   