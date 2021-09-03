"""Post graphql types"""

# Django
import django_filters

# Graphene
import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

# Models
from mydea.posts.models import Post
from mydea.utils.models import MyDeaModel

# Django-raphql-auth
from graphql_auth.schema import UserNode


# #test
# class Abstract(DjangoObjectType):
#     class Meta:
#         model = MyDeaModel
#         filter_fields = ('hello', )
    
#     hello = graphene.String()

#     def resolve_hello(self, info):
#         return 'hello'

# Post types
class PostNode(DjangoObjectType):
    class Meta:
        model = Post        
        filter_fields = ('created_by__username',)
        interfaces = (relay.Node, ) 
    
    created_by = graphene.Field(UserNode)










   