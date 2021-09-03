"""Post graphql mutations"""

# Django
from django.core.exceptions import (
    ValidationError,    
)

# Graphene
import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphql_relay import from_global_id

# Django-graphql-auth
from graphql_jwt.decorators import login_required

# Types
from .types import PostNode

# Models
from mydea.posts.models import Post
from mydea.users.models import User

# Errors
from mydea.utils.errors import Error, format_validation_errors


class CreatePostMutation(relay.ClientIDMutation):
    """Post mutation for creating an post"""
    post = graphene.Field(PostNode)

    class Input:        
        visibility = graphene.String(required=False)
        body = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(Error)    

    @login_required
    def mutate_and_get_payload(root, info, **input):
        try:               
            input_data = {**input}            
            # This ensures default visibility value from model (PB - Public)
            if "visibility" in input_data and input_data["visibility"] is None: 
                input_data.pop("visibility") 
            # Get user
            user = info.context.user                      
            # Create post object            
            post = Post(
                created_by = user,
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


class UpdatePostMutation(relay.ClientIDMutation):
    """Post mutation for updating the visibility of a post"""
    post = graphene.Field(PostNode)

    class Input:     
        id = graphene.ID(required=True)   
        visibility = graphene.String(required=True)        

    success = graphene.Boolean()
    errors = graphene.List(Error)    

    @login_required
    def mutate_and_get_payload(root, info, id, visibility):
        try:
            # Get post
            post = Post.objects.get(pk=from_global_id(id)[1])
            # Update visibility
            post.visibility = visibility
            post.full_clean()
            post.save()

            return UpdatePostMutation(success=True, post=post)
        
        except ValidationError as e:
            # Format all validations errors
            errors = format_validation_errors(e)
            return CreatePostMutation(success=False, errors=errors)


# Post mutations
class PostMutation(graphene.ObjectType):
    create_post = CreatePostMutation.Field()
    edit_visibility = UpdatePostMutation.Field()

