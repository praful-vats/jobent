from django.db import models
from django.contrib.auth.models import User

# Define the UserProfile model to store additional user information
class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('premium', 'Premium'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')
    is_premium = models.BooleanField(default=False)  # Default is normal user
    tokens = models.IntegerField(default=100)  # All users start with 100 tokens

    def __str__(self):
        return f"{self.user.username}'s profile"
    def __str__(self):
        return f"{self.user.username} - {self.user_type} (Tokens: {self.premium_tokens})"
