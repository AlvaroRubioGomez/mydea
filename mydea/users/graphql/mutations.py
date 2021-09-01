"""User graphql mutations"""

# Models
from mydea.users.models import User

# Graphql-auth
from graphql_auth.mutations import Register


class AutoVerificationRegister(Register):
    """
    Register user with fields defined in the settings.

    If the email field of the user model is part of the
    registration fields (default), check if there is
    no user with that email or as a secondary email.

    If it exists, it does not register the user,
    even if the email field is not defined as unique
    (default of the default django user model).

    When creating the user, it also creates a `UserStatus`
    related to that user, making it possible to track
    if the user is archived, verified and has a secondary
    email.

    When creating the user, it sets the `UserStatus` verified
    flag as true.

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

        # Verified user
        if response.success:
            username = kwargs.get("username")
            user = User.objects.get(username=username)            
            user.status.verified = True
            user.status.save(update_fields=["verified"])        
        
        return response




