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

# # Profile queries
# class ProfileQueries(graphene.ObjectType):
#     following = DjangoFilterConnectionField(CustomUserNode)
#     followers = DjangoFilterConnectionField(CustomUserNode)

#     @login_required    
#     def resolve_following(root, info):       
#         user = info.context.user     
#         return user.profile.following.all()      
    
#     @login_required    
#     def resolve_followers(root, info):       
#         user = info.context.user     
#         return user.profile.followers.all()   
        