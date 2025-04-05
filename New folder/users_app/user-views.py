from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserCreateSerializer

User = get_user_model()

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow or unfollow a user based on POST request
    """
    target_user = get_object_or_404(User, pk=user_id)
    current_user = request.user
    
    # Don't allow users to follow themselves
    if target_user == current_user:
        return Response(
            {'error': 'You cannot follow yourself.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if already following and toggle
    if current_user in target_user.followers.all():
        target_user.followers.remove(current_user)
        action = 'unfollowed'
    else:
        target_user.followers.add(current_user)
        action = 'followed'
    
    return Response({
        'status': 'success',
        'action': action,
        'user': UserSerializer(target_user).data
    })

@api_view(['GET'])
def user_followers(request, user_id):
    """
    Get all followers of a specific user
    """
    user = get_object_or_404(User, pk=user_id)
    followers = user.followers.all()
    serializer = UserSerializer(followers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user_following(request, user_id):
    """
    Get all users that a specific user is following
    """
    user = get_object_or_404(User, pk=user_id)
    following = user.following.all()
    serializer = UserSerializer(following, many=True)
    return Response(serializer.data)
