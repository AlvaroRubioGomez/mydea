"""User graphql mutations"""

# Graphene
import graphene

# Graphql-auth
from graphql_auth import mutations

# Models
from mydea.users.models import User, Profile


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
        
        return response


# Auth mutations
class AuthMutation(graphene.ObjectType):
    register = AutoVerificationRegister.Field() #override register
    login = mutations.ObtainJSONWebToken.Field()
    password_change = mutations.PasswordChange.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()


