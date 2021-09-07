"""Connections model"""

# Django
from django.db import models

# Utilities
from mydea.utils.models import MyDeaModel


class Connection(MyDeaModel):
    """Connection model.
    A connection holds the information about 
    a user's followers and following users"""

    # user
    user = models.OneToOneField('users.User', on_delete=models.CASCADE) 

    # connections
    following = models.ManyToManyField(
        'users.User', 
        blank=True, 
        related_name='following'
    )  
    followers = models.ManyToManyField(
        'users.User', 
        blank=True, 
        related_name='followers'
    )  

    def __str__(self):
        """Return user's connections."""        
        return f"{self.user}: -->{list(self.following.all())} / <--{list(self.followers.all())}"