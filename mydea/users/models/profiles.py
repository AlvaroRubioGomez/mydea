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

    # Publications
    posts = models.ForeignKey(
        'posts.Post', 
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
