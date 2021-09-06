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
from mydea.users.models import User

# Errors
from mydea.utils.errors import Error, format_validation_errors


# variables
class Action(graphene.Enum):
    accept = 'A'
    reject = 'R'

# Request mutations

class CreateRequestMutation(relay.ClientIDMutation):
    """Request mutation for creating a request"""
    request = graphene.Field(RequestNode)

    class Input:        
        to_user_id = graphene.ID(required=True)        

    success = graphene.Boolean()
    errors = graphene.List(Error)    

    @login_required
    def mutate_and_get_payload(root, info, to_user_id):
        try:            
            # Get sender user            
            s_user = info.context.user  
            # Get receiver user
            r_user =  User.objects.get(
                pk=from_global_id(to_user_id)[1]
            )                             
            # Create request object            
            request = Request(
                sender = s_user,
                receiver = r_user         
            )          
            # Validate all fields
            request.full_clean()
            request.save()            

            return CreateRequestMutation(success=True, request=request)

        except ValidationError as e:
            # Format all validations errors
            errors = format_validation_errors(e)
            return CreateRequestMutation(success=False, errors=errors)


class UpdateRequestMutation(relay.ClientIDMutation):
    """Request mutation for accepting a follow request"""  
    request = graphene.Field(RequestNode) 

    class Input:     
        request_id = graphene.ID(required=True) 
        action = Action(required=True)              

    success = graphene.Boolean()
    errors = graphene.List(Error)    

    @login_required  
    def mutate_and_get_payload(root, info, request_id, action):
        try:
            # Get user
            user = info.context.user
            # Get request
            request = Request.objects.get(pk=from_global_id(request_id)[1])

            # Accept request
            if action == 'A':  
                # Update status
                request.status = 'A' 
                # Add sender to user's followers 
                user.connection.followers.add(request.sender)
                user.save()
                # Add user to receiver's following
                request.sender.connection.following.add(user)
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
    send_request = CreateRequestMutation.Field()


# Connections mutations

class DeleteFollowingMutation(relay.ClientIDMutation):
    """Post mutation for deleting a user's following 
    (i.e stop following a user)"""    

    class Input:     
        user_id = graphene.ID(required=True)               

    success = graphene.Boolean()
    errors = graphene.List(Error)    

    @login_required  
    def mutate_and_get_payload(root, info, user_id):
        #try:        
        # Get request user
        user = info.context.user
        # Get following user            
        f_user = User.objects.get(pk=from_global_id(user_id)[1])                     
        # Delete f_user from user's following         
        user.connection.following.remove(f_user)
        user.save()
        # Delete user from f_user's followers        
        f_user.connection.followers.remove(user)  
        f_user.save()   

        return DeleteFollowingMutation(success=True)    


class DeleteFollowersMutation(relay.ClientIDMutation):
    """Post mutation for deleting a user's follower 
    (i.e a user stops following you)"""    

    class Input:     
        user_id = graphene.ID(required=True)               

    success = graphene.Boolean()
    errors = graphene.List(Error)    

    @login_required    
    def mutate_and_get_payload(root, info, user_id):
        #try:        
        # Get request user
        user = info.context.user
        # Get follower user            
        f_user = User.objects.get(pk=from_global_id(user_id)[1])                     
        # Delete f_user from user's followers         
        user.connection.followers.remove(f_user)
        user.save()
        # Delete user from f_user's followings        
        f_user.connection.following.remove(user)  
        f_user.save()   

        return DeleteFollowersMutation(success=True)         
      

class ConnectionMutation(graphene.ObjectType):
    delete_following = DeleteFollowingMutation.Field()
    delete_followers = DeleteFollowersMutation.Field()

