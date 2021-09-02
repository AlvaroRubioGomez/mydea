"""Main schema module."""

# Graphene
import graphene
from graphene import relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField

# Django-graphql-auth
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery

# Types
from mydea.posts.graphql.types import PostNode

# Queries

# Mutations
from mydea.users.graphql.mutations import AutoVerificationRegister
from mydea.posts.graphql.mutations import CreatePostMutation

# Queries
class PostQuery(ObjectType):
    """Post queries"""
    post = relay.Node.Field(PostNode)
    posts = DjangoFilterConnectionField(PostNode)

# Mutations
class AuthMutation(graphene.ObjectType):
    register = AutoVerificationRegister.Field() #custom register
    login = mutations.ObtainJSONWebToken.Field()
    password_change = mutations.PasswordChange.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()

class PostMutation(graphene.ObjectType):
    create_post = CreatePostMutation.Field()


class Query(
    UserQuery,
    MeQuery, 
    PostQuery,
    graphene.ObjectType):
    pass

class Mutation(
    AuthMutation,  
    PostMutation, 
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
