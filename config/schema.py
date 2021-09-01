"""Main schema module."""

# Graphene
import graphene

# Django-graphql-auth
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery

# Queries

# Mutations
from mydea.users.graphql.mutations import AutoVerificationRegister


class AuthMutation(graphene.ObjectType):
    register = AutoVerificationRegister.Field() #custom register
    login = mutations.ObtainJSONWebToken.Field()
    password_change = mutations.PasswordChange.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()

class Query(
    UserQuery,
    MeQuery, 
    graphene.ObjectType):
    pass

class Mutation(
    AuthMutation,    
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
