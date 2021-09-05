"""Main schema module."""

# Graphene
import graphene

# Django-graphql-auth
# from graphql_auth.schema import UserQuery

# Queries
from mydea.users.graphql.queries import UsersQuery, ProfileQueries
from mydea.posts.graphql.queries import PostsQuery
from mydea.socials.graphql.queries import RequestsQuery

# Mutations
from mydea.users.graphql.mutations import AuthMutation, ProfileMutation
from mydea.posts.graphql.mutations import PostMutation
from mydea.socials.graphql.mutations import RequestMutation


class Query(   
    UsersQuery,
    PostsQuery,
    ProfileQueries,
    RequestsQuery,
    graphene.ObjectType):
    pass

class Mutation(
    AuthMutation,  
    PostMutation, 
    ProfileMutation,
    RequestMutation,
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
