"""User profile model"""

# Django
from django.db import models

# Utilities
from mydea.utils.models import MyDeaModel


class Profile(MyDeaModel):
    """Profile model.
    A profile holds a user's data like biography, picture,
    published posts, notifications and social data."""

    # Info
    user = models.OneToOneField('users.User', on_delete=models.CASCADE) 

    # # Connections
    # following = models.ManyToManyField(
    #     'users.User', 
    #     blank=True, 
    #     related_name='following'
    # )  
    # followers = models.ManyToManyField(
    #     'users.User', 
    #     blank=True, 
    #     related_name='followers'
    # )  

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
