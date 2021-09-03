"""Main schema module."""

# Graphene
import graphene

# Django-graphql-auth
from graphql_auth.schema import UserQuery, MeQuery

# Queries
from mydea.posts.graphql.queries import PostsQuery

# Mutations
from mydea.users.graphql.mutations import AuthMutation
from mydea.posts.graphql.mutations import PostMutation


class Query(
    UserQuery,
    MeQuery, 
    PostsQuery,
    graphene.ObjectType):
    pass

class Mutation(
    AuthMutation,  
    PostMutation, 
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
