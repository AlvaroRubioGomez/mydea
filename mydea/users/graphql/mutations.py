"""User graphql mutations"""

# Django
from django.core.exceptions import (
    ValidationError,    
)

# Graphene
import graphene
from graphene import relay
from graphql_relay import from_global_id

# Graphql-auth
from graphql_auth import mutations
from graphql_jwt.decorators import login_required

# Models
from mydea.users.models import User, Profile
from mydea.socials.models import Connection

# # Types
# from .types import ProfileNode

# Errors
from mydea.utils.errors import Error, format_validation_errors


# Auth mutations

class AutoVerificationRegister(mutations.Register):
    """
    Register user with fields defined in the settings.

    If the email field of the user model is part of the
    registration fields (default), check if there is
    no user with that email or as a secondary email.

    If it exists, it does not register the user,
    even if the email field is not defined as unique
    (default of the default django user model).

    When creating the user:
    + creates a `UserStatus`
    related to that user, making it possible to track
    if the user is archived, verified and has a secondary
    email.
    + sets the `UserStatus` verified
    flag as true.
    + creates an empty profile associated with the registered 
    user.

    Send account verification email.    
    """
    
    @classmethod
    def set_doc(cls):
        """Set the graphqlapi docs from the class docs"""
        __doc__ = cls.__doc__

    @classmethod
    def mutate(cls, root, info, **kwargs):
        # Get Register mutation response
        response = super().resolve_mutation(root, info, **kwargs)

        if response.success:
            # Get user            
            username = kwargs.get("username")
            user = User.objects.get(username=username)   
            # Verified user         
            user.status.verified = True
            user.status.save(update_fields=["verified"])    
            # Create profile with user
            profile = Profile.objects.create(user=user) 
            profile.save()  
            # Create empty connection for user
            connection = Connection.objects.create(user=user)
            connection.save()
        
        return response


class AuthMutation(graphene.ObjectType):
    register = AutoVerificationRegister.Field() #override register
    login = mutations.ObtainJSONWebToken.Field()
    password_change = mutations.PasswordChange.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()


# # Profile mutations

# class DeleteFollowingMutation(relay.ClientIDMutation):
#     """Post mutation for deleting a user's following 
#     (i.e stop following a user)"""    

#     class Input:     
#         user_id = graphene.ID(required=True)               

#     success = graphene.Boolean()
#     errors = graphene.List(Error)    

#     @login_required  
#     def mutate_and_get_payload(root, info, user_id):
#         #try:        
#         # Get request user
#         user = info.context.user
#         # Get following user            
#         f_user = User.objects.get(pk=from_global_id(user_id)[1])                     
#         # Delete f_user from user's following         
#         user.profile.following.remove(f_user)
#         user.save()
#         # Delete user from f_user's followers        
#         f_user.profile.followers.remove(user)  
#         f_user.save()   

#         return DeleteFollowingMutation(success=True)    


# class DeleteFollowersMutation(relay.ClientIDMutation):
#     """Post mutation for deleting a user's follower 
#     (i.e a user stops following you)"""    

#     class Input:     
#         user_id = graphene.ID(required=True)               

#     success = graphene.Boolean()
#     errors = graphene.List(Error)    

#     @login_required    
#     def mutate_and_get_payload(root, info, user_id):
#         #try:        
#         # Get request user
#         user = info.context.user
#         # Get follower user            
#         f_user = User.objects.get(pk=from_global_id(user_id)[1])                     
#         # Delete f_user from user's followers         
#         user.profile.followers.remove(f_user)
#         user.save()
#         # Delete user from f_user's followings        
#         f_user.profile.following.remove(user)  
#         f_user.save()   

#         return DeleteFollowersMutation(success=True)         
      

# class ProfileMutation(graphene.ObjectType):
#     delete_following = DeleteFollowingMutation.Field()
#     delete_followers = DeleteFollowersMutation.Field()
