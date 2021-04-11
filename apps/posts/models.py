from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    caption = models.CharField(max_length=200, default='', verbose_name='内容')
    tags = models.CharField(max_length=100, null=True, blank=True, verbose_name='标签')
    createdAt = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    
    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = verbose_name


class PostFile(models.Model):
    url = models.CharField(max_length=200, default='', verbose_name='文件地址')
    post = models.ForeignKey(Post, related_name='files', verbose_name='文件', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = '文件'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    text = models.CharField(max_length=140, default='', verbose_name='评论')
    post = models.ForeignKey(Post, related_name='comments', verbose_name='帖子', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name


class Like(models.Model):
    post = models.ForeignKey(Post, verbose_name='帖子', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __str__(self):
        return self.post.caption

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name


class Follow(models.Model):
    following = models.ForeignKey(User, related_name='following', verbose_name='被关注者', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, verbose_name='关注者', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __str__(self):
        return self.following.username

    class Meta:
        verbose_name = '关注'
        verbose_name_plural = verbose_name


class Save(models.Model):
    post = models.ForeignKey(Post, verbose_name='帖子', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    def __str__(self):
        return self.post.caption

    class Meta:
        verbose_name = '保存'
        verbose_name_plural = verbose_name