from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser



class UserModel(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']
        indexes = [
            models.Index(fields=['username']),
        ]
