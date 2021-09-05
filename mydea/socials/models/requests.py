"""Request model"""

# Django
from django.db import models

# Utilities
from mydea.utils.models import MyDeaModel


class Request(MyDeaModel):
    """Request model.
    A request is an user follow request to another user
    It has three possible states:
        + sent: A request that has been sent and an action
        is required to be taken.
        + accepted: A request that has been accepted.
        + rejected: A request that has been rejected"""

    STATUS_CHOICES = [
        ('S', 'sent'),
        ('A', 'accepted'),
        ('R', 'rejected')
    ]

    sender = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='sender'
    )

    receiver = models.ForeignKey(
        'users.User',   
        on_delete=models.CASCADE, 
        related_name='receiver'
    ) 
   
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='S',
        # blank=True,
        # null=True
    )    

    def __str__(self):
        """Return request sender, receiver and status"""
        return f"{self.sender} --> {self.receiver} : {self.status}"