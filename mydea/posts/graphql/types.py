"""Post graphql types"""

# Django
import django_filters

# Graphene
import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from graphql_jwt.decorators import login_required

# Models
from mydea.posts.models import Post

# Types
from mydea.users.graphql.types import ProfileNode

# Post types
class PostNode(DjangoObjectType):
    class Meta:
        model = Post        
        filter_fields = []
        interfaces = (relay.Node, )   
    
    created_by = graphene.Field(ProfileNode)