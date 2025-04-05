from rest_framework import serializers
from .models import Tweet, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    author_profile_image = serializers.ImageField(source='author.profile_image', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'tweet', 'author', 'author_username', 'author_profile_image', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']


class TweetSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    author_profile_image = serializers.ImageField(source='author.profile_image', read_only=True)
    like_count = serializers.ReadOnlyField()
    comments = CommentSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Tweet
        fields = ['id', 'author', 'author_username', 'author_profile_image', 'content', 
                  'created_at', 'updated_at', 'like_count', 'comments', 'is_liked']
        read_only_fields = ['author', 'created_at', 'updated_at']
    
    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user in obj.likes.all()
        return False
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class TweetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content']
