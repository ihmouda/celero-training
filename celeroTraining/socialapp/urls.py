from django.urls import path, include
from .views import FriendshipRequestViewSet, BlockViewSet, UserBlockViewSet, UserFriendshipViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'friend-requests', FriendshipRequestViewSet, basename='friendship-requests')
router.register(r'blocks', BlockViewSet, basename='block')

urlpatterns = [

    path('', include(router.urls)),

    path('users/<pk>/friendships', UserFriendshipViewSet.as_view({'get': 'list'})),
    path('users/<pk>/blocks', UserBlockViewSet.as_view({'get': 'list'})),
]