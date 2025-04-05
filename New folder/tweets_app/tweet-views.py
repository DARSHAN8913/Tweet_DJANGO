from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Tweet, Comment
from .serializers import TweetSerializer, TweetCreateSerializer, CommentSerializer
from django.db.models import Q

class TweetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Tweet instances.
    """
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'author__username']
    ordering_fields = ['created_at', 'like_count']
    
    def get_queryset(self):
        # By default, return all tweets
        queryset = Tweet.objects.all()
        
        # Filter by user if username query param is provided
        username = self.request.query_params.get('username')
        if username:
            queryset = queryset.filter(author__username=username)
        
        # Filter for followed users' tweets if "following" param is provided
        following = self.request.query_params.get('following')
        if following and self.request.user.is_authenticated:
            followed_users = self.request.user.following.all()
            queryset = queryset.filter(author__in=followed_users)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TweetCreateSerializer
        return TweetSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        tweet = self.get_object()
        user = request.user
        
        if user in tweet.likes.all():
            tweet.likes.remove(user)
            return Response({'status': 'unliked'})
        else:
            tweet.likes.add(user)
            return Response({'status': 'liked'})
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        tweet = self.get_object()
        comments = tweet.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        tweet = self.get_object()
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(author=request.user, tweet=tweet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed(request):
    """
    Returns tweets from the authenticated user and those they follow
    """
    user = request.user
    following_users = user.following.all()
    
    # Get tweets from user and followed users
    tweets = Tweet.objects.filter(
        Q(author=user) | Q(author__in=following_users)
    ).order_by('-created_at')
    
    serializer = TweetSerializer(tweets, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def trending(request):
    """
    Returns the most liked tweets in the last 24 hours
    """
    from django.utils import timezone
    from datetime import timedelta
    
    last_24h = timezone.now() - timedelta(days=1)
    tweets = Tweet.objects.filter(created_at__gte=last_24h).order_by('-like_count')[:10]
    
    serializer = TweetSerializer(tweets, many=True, context={'request': request})
    return Response(serializer.data)
