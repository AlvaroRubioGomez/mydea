"""Request graphql queries"""

# Graphene
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay

# Django-graphql-auth
from graphql_jwt.decorators import login_required

# Types
from .types import RequestNode
from mydea.users.graphql.types import CustomUserNode

# Models
from mydea.users.models import User
from mydea.socials.models import Request, Connection

# Requests queries

class RequestsQuery(graphene.ObjectType):        
    my_requests = DjangoFilterConnectionField(RequestNode)    
    
    @login_required    
    def resolve_my_requests(root, info):       
        user = info.context.user         
        my_requests = Request.objects.filter(
            receiver=user,
            status='S'
        ).all()        
        return my_requests

# Connections queries

class ConnectionQuery(graphene.ObjectType):
    my_following = DjangoFilterConnectionField(CustomUserNode)
    my_followers = DjangoFilterConnectionField(CustomUserNode)    

    @login_required    
    def resolve_my_following(root, info):       
        user = info.context.user                
        my_following = user.connection.following        
        return my_following  
    
    @login_required    
    def resolve_my_followers(root, info):       
        user = info.context.user         
        my_followers = user.connection.followers        
        return my_followers  
        
        