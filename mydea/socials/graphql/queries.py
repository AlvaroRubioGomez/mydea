"""Request graphql queries"""

# Graphene
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay

# Django-graphql-auth
from graphql_jwt.decorators import login_required

# Types
from .types import RequestNode 

# Models
from mydea.users.models import User
from mydea.socials.models import Request


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
        
        