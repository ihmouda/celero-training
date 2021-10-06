from django.urls import path
from .views import CreateFriendshipRequest, UpdateFriendshipRequest, UserFriends, UserBlocked, CreateBlock, UpdateBlock

urlpatterns = [

    path('friend-requests', CreateFriendshipRequest.as_view(), name='friendship request'),
    path('friend-requests/<pk>', UpdateFriendshipRequest.as_view(), name='friendship request'),

    path('blocks', CreateBlock.as_view(), name='block user'),
    path('blocks/<pk>', UpdateBlock.as_view(), name='block user'),

    path('users/<pk>/friends', UserFriends.as_view(), name='friends'),
    path('users/<pk>/blocked', UserBlocked.as_view(), name='blocked'),
]