"""User profile model"""

# Django
from django.db import models

# Utilities
from mydea.utils.models import MyDeaModel


class Profile(MyDeaModel):
    """Profile model.
    A profile holds a user's data"""

    # user
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)     

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)