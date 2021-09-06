"""Main schema module."""

# Graphene
import graphene

# Queries
from mydea.users.graphql.queries import UsersQuery
from mydea.posts.graphql.queries import PostsQuery
from mydea.socials.graphql.queries import (
    RequestsQuery, 
    ConnectionQuery
)

# Mutations
from mydea.users.graphql.mutations import AuthMutation
from mydea.posts.graphql.mutations import PostMutation
from mydea.socials.graphql.mutations import (
    RequestMutation,
    ConnectionMutation
)


class Query(   
    UsersQuery,
    PostsQuery,
    ConnectionQuery,
    RequestsQuery,
    graphene.ObjectType):
    pass

class Mutation(
    AuthMutation,  
    PostMutation, 
    ConnectionMutation,
    RequestMutation,
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
