from django.contrib import admin
from .models import Profile, Post, Comment, Like, Follower

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    search_fields = ['user__username']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'caption', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'caption']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'comment_text', 'created_at']
    search_fields = ['user__username']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']

@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    search_fields = ['follower__username', 'following__username']