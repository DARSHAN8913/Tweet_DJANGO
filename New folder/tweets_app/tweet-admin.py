from django.contrib import admin
from .models import Tweet, Comment

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'content_preview', 'created_at', 'like_count']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username']
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'tweet', 'author', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username', 'tweet__content']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
