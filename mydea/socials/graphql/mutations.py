"""Request graphql mutations"""

# Django
from django.core.exceptions import (
    ValidationError,    
)

# Graphene
import graphene
from graphene import relay
from graphql_relay import from_global_id

# Django-graphql-auth
from graphql_jwt.decorators import login_required

# Types
from .types import RequestNode

# Models
from mydea.socials.models import Request

# Errors
from mydea.utils.errors import Error, format_validation_errors


# variables
class Action(graphene.Enum):
    accept = 'A'
    reject = 'R'

# Request mutations
class UpdateRequestMutation(relay.ClientIDMutation):
    """Request mutation for accepting a follow request"""  
    request = graphene.Field(RequestNode) 

    class Input:     
        r_id = graphene.ID(required=True) 
        action = Action(required=True)              

    success = graphene.Boolean()
    errors = graphene.List(Error)    

    @login_required  
    def mutate_and_get_payload(root, info, r_id, action):
        try:
            # Get user
            user = info.context.user
            # Get request
            request = Request.objects.get(pk=from_global_id(r_id)[1])

            # Accept request
            if action == 'A':  
                # Update status
                request.status = 'A' 
                # Add sender to user's followers 
                user.profile.followers.add(request.sender)
                user.save()
                # Add user to receiver's following
                request.sender.profile.following.add(user)
                user.save()

            # Reject request
            if action == 'R':  
                request.status = 'R'

            # Validate all fields
            request.full_clean()      
            request.save()

            return UpdateRequestMutation(success=True, request=request)  

        except ValidationError as e:
            # Format all validations errors
            errors = format_validation_errors(e)
            return UpdateRequestMutation(success=False, errors=errors) 

# Request mutations
class RequestMutation(graphene.ObjectType):
    resolve_request = UpdateRequestMutation.Field()

