
from django.contrib import admin
from .models import Profile, Post, Like_post, FollowerCount, Bookmarks, Message, Stories

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like_post)
admin.site.register(FollowerCount)
admin.site.register(Bookmarks)
admin.site.register(Message)
admin.site.register(Stories)