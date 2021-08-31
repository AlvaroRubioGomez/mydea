"""Errors type and functions"""

# Graphene
import graphene

# Error type
class Error(graphene.ObjectType):
    field_name = graphene.String()
    messages = graphene.List(graphene.String)

# Error functions
def format_validation_errors(e):
    """Return a graphene list of Error type from a validation error object"""
    return [Error(field_name=field_name, messages=e.message_dict[field_name])
                for field_name in e.message_dict]
