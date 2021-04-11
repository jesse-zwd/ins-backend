from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=50, default='', verbose_name='昵称')
    email = models.EmailField(max_length=50, default='', verbose_name='邮箱')
    avatar = models.CharField(max_length=100, default='', verbose_name='头像')
    bio = models.CharField(max_length=200, null=True, blank=True, verbose_name='个人介绍')
    website = models.CharField(max_length=50, null=True, blank=True, verbose_name='网站')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name