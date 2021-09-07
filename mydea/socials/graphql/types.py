"""Social graphql types"""

# Django
import django_filters

# Graphene
import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

from graphql_jwt.decorators import login_required

# Models
from mydea.socials.models import Request

# Request types
class RequestNode(DjangoObjectType):
    class Meta:
        model = Request               
        filter_fields = []
        interfaces = (relay.Node, )   