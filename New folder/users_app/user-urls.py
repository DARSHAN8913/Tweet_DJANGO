from django.urls import path
from . import views

urlpatterns = [
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/profile/', views.UserUpdateView.as_view(), name='user-update'),
    path('users/<str:username>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/<int:user_id>/follow/', views.follow_user, name='follow-user'),
    path('users/<int:user_id>/followers/', views.user_followers, name='user-followers'),
    path('users/<int:user_id>/following/', views.user_following, name='user-following'),
]
