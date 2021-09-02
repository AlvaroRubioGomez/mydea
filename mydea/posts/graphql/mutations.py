"""Post graphql mutations"""

# Django
from django.core.exceptions import ValidationError

# Graphene
import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType

# # Django-graphql-auth
# from graphql_jwt.decorators import login_required

# Types
from .types import PostNode

# Models
from mydea.posts.models import Post
from mydea.users.models import User

# Errors
from mydea.utils.errors import Error, format_validation_errors

#@login_required
class CreatePostMutation(relay.ClientIDMutation):
    """Post mutation for creating an post"""
    post = graphene.Field(PostNode)

    class Input:        
        visibility = graphene.String(required=False)
        body = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(Error)    

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:   
            # Get visibility
            input_data = {**input}
            if input_data['visibility'] is None: 
                input_data.pop('visibility') # This ensures default visibility value from model
            # Get user
            request_user = info.context.user                      
            # Create post object            
            post = Post(
                created_by = request_user,
                **input_data          
            )          
            # Validate all fields
            post.full_clean()
            post.save()

            return CreatePostMutation(success=True, post=post)

        except ValidationError as e:
            # Format all validations errors
            errors = format_validation_errors(e)

            return CreatePostMutation(success=False, errors=errors)

