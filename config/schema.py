"""Main schema module."""

# Graphene
import graphene

# Django-graphql-auth
# from graphql_auth.schema import UserQuery

# Queries
from mydea.users.graphql.queries import UsersQuery, ProfileQueries
from mydea.posts.graphql.queries import PostsQuery

# Mutations
from mydea.users.graphql.mutations import AuthMutation, ProfileMutation
from mydea.posts.graphql.mutations import PostMutation


class Query(   
    UsersQuery,
    PostsQuery,
    ProfileQueries,
    graphene.ObjectType):
    pass

class Mutation(
    AuthMutation,  
    PostMutation, 
    ProfileMutation,
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
