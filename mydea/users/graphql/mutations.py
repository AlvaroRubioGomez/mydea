"""User graphql mutations"""

# Models
from mydea.users.models import User

# Graphql-auth
from graphql_auth.mutations import Register


class AutoVerificationRegister(Register):

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




