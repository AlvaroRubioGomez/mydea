"""User graphql types"""

# Graphene
import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType

# Models
from mydea.users.models import User

# Node types
class UserNode(DjangoObjectType):
    class Meta:
        model = User
        #exclude = ['password']
        filter_fields = ['username', 'email']
        interfaces = (relay.Node, )

    def resolve_password(self, info):
        requested_user = info.context.user
        if requested_user.email == 'admin@gmail.com':
            return self.password
        return None


# Input types
class CreateUserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    phone_number = graphene.String(required=False)

class UpdateUserInput(graphene.InputObjectType):
    username = graphene.String(required=False)
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)
    email = graphene.String(required=False)
    phone_number = graphene.String(required=False)




