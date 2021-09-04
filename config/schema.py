"""Main schema module."""

# Graphene
import graphene

# Django-graphql-auth
# from graphql_auth.schema import UserQuery

# Queries
from mydea.posts.graphql.queries import PostsQuery
from mydea.users.graphql.queries import UsersQuery

# Mutations
from mydea.users.graphql.mutations import AuthMutation
from mydea.posts.graphql.mutations import PostMutation


class Query(   
    UsersQuery,
    PostsQuery,
    graphene.ObjectType):
    pass

class Mutation(
    AuthMutation,  
    PostMutation, 
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
