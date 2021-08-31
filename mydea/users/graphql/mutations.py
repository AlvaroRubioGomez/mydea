"""User graphql mutations"""

# Django
from django.core.exceptions import ValidationError

# Graphene
import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id
from graphql import GraphQLError

# Types
from .types import UserNode, CreateUserInput, UpdateUserInput

# Models
from mydea.users.models import User

# Errors
from mydea.utils.errors import Error, format_validation_errors


class CreateUserMutation(relay.ClientIDMutation):
    """User mutation for creating an user"""
    class Input:
        user_data = CreateUserInput()

    user = graphene.Field(UserNode)
    errors = graphene.List(Error)

    @classmethod
    def mutate_and_get_payload(cls, root, info, user_data):
        try:
            # Create user object
            user = User(
                username = user_data.username,
                first_name = user_data.first_name,
                last_name = user_data.last_name,
                email = user_data.email,
                password = user_data.password,
                phone_number = user_data.phone_number,
            )
            # Validate all fields
            user.full_clean()
            user.save()

            return CreateUserMutation(user=user)

        except ValidationError as e:
            # Format all validations errors
            errors = format_validation_errors(e)

            return CreateUserMutation(errors=errors)


class UpdateUserMutation(relay.ClientIDMutation):
    """User mutation for updating an user"""
    class Input:
        user_data = UpdateUserInput()
        id = graphene.ID(required=True)

    user = graphene.Field(UserNode)
    errors = graphene.List(Error)

    @classmethod
    def mutate_and_get_payload(cls, root, info, user_data, id):
        # Get user
        user = User.objects.get(pk=from_global_id(id)[1])

        # Set user attributes
        for attr, value in user_data.items():
            setattr(user, attr, value)

        try:
            # Validate all fields
            user.full_clean()
            user.save()

            return UpdateUserMutation(user=user)

        except ValidationError as e:
            # Format all validations errors
            errors = format_validation_errors(e)

            return UpdateUserMutation(errors=errors)


class UserMutation(ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
