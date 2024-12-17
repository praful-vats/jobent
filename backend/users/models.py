from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('premium', 'Premium'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')
    premium_tokens = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.user.username} - {self.user_type} (Tokens: {self.premium_tokens})"
