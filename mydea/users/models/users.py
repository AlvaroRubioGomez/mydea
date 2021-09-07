"""User model"""

# Django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Utilities
from mydea.utils.models import MyDeaModel

class User(MyDeaModel, AbstractUser):
    """User model.
    Extend from Django's Abstract Base User by adding some extra fields.
    """

    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        blank=True, 
        null=True
    )

    
    def __str__(self):
        """Return username."""
        return self.username