from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=50, default='', verbose_name='nickname')
    email = models.EmailField(max_length=50, default='', verbose_name='email')
    avatar = models.CharField(max_length=100, default='', verbose_name='avatar')
    bio = models.CharField(max_length=200, null=True, blank=True, verbose_name='bio')
    website = models.CharField(max_length=50, null=True, blank=True, verbose_name='website')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = verbose_name