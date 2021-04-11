from django.contrib import admin

from .models import Post, PostFile, Comment, Like, Follow

# Register your models here.
admin.site.register(PostFile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
