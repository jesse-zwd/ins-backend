from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    caption = models.CharField(max_length=200, default='', verbose_name='caption')
    tags = models.CharField(max_length=100, null=True, blank=True, verbose_name='tags')
    createdAt = models.DateTimeField(default=datetime.now, verbose_name='createdAt')
    
    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = verbose_name


class PostFile(models.Model):
    url = models.CharField(max_length=200, default='', verbose_name='url')
    post = models.ForeignKey(Post, related_name='files', verbose_name='files', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=datetime.now, verbose_name='createdAt')

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'files'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    text = models.CharField(max_length=140, default='', verbose_name='comment')
    post = models.ForeignKey(Post, related_name='comments', verbose_name='post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=datetime.now, verbose_name='createdAt')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = verbose_name


class Like(models.Model):
    post = models.ForeignKey(Post, verbose_name='post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=datetime.now, verbose_name='createdAt')

    def __str__(self):
        return self.post.caption

    class Meta:
        verbose_name = 'like'
        verbose_name_plural = verbose_name


class Follow(models.Model):
    following = models.ForeignKey(User, related_name='following', verbose_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, verbose_name='follower', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=datetime.now, verbose_name='createdAt')

    def __str__(self):
        return self.following.username

    class Meta:
        verbose_name = 'follow'
        verbose_name_plural = verbose_name


class Save(models.Model):
    post = models.ForeignKey(Post, verbose_name='post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=datetime.now, verbose_name='createdAt')

    def __str__(self):
        return self.post.caption

    class Meta:
        verbose_name = 'save'
        verbose_name_plural = verbose_name