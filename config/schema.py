"""Main schema module."""

# Graphene
import graphene

# Django-graphql-auth
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery

# Queries

# Mutations


class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field()  
   login = mutations.ObtainJSONWebToken.Field()

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
