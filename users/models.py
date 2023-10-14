from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    profile_image = models.ImageField(upload_to='profile',blank=True,null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']