from django.urls import path, include
from .views import FriendshipRequestViewSet, FriendshipViewSet, UserFriendshipViewSet, UserBlockViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'friends', FriendshipViewSet, basename='block')
router.register(r'friend-requests', FriendshipRequestViewSet, basename='friendship-requests')

urlpatterns = [

    path('', include(router.urls)),

    path('users/<pk>/friendships', UserFriendshipViewSet.as_view({'get': 'list'})),
    path('users/<pk>/blocks', UserBlockViewSet.as_view({'get': 'list'})),
]