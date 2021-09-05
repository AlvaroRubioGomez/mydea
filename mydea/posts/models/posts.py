"""Post model"""

# Django
from django.db import models

# Utilities
from mydea.utils.models import MyDeaModel


class Post(MyDeaModel):
    """Post model.
    A post is an user publication that contains a body text and
    it is visible depending on its visibility property:
        + public: Everybody can see it
        + protected: Only user followers can see it
        + private: Only the owner can see it"""

    VISIBILITY_CHOICES = [
        ('PB', 'public'),
        ('PT', 'protected'),
        ('PV', 'private')
    ]

    created_by = models.ForeignKey('users.Profile', on_delete=models.CASCADE)  
   
    visibility = models.CharField(
        max_length=2,
        choices=VISIBILITY_CHOICES,
        default='PB',
        blank=True,
        null=True
    )

    body = models.CharField(max_length=280, blank=True)   
    

    def __str__(self):
        """Return user's str representation."""
        return str(self.created_by.user.username)