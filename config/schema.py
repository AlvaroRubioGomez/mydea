"""Main schema module."""

# Graphene
import graphene

# Queries
from mydea.users.graphql.queries import UserQuery

# Mutations
from mydea.users.graphql.mutations import UserMutation


class Query(UserQuery, graphene.ObjectType):
    pass

class Mutation(UserMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
