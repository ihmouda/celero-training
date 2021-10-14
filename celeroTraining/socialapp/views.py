from rest_framework import generics, viewsets, status
from .serializers import FriendshipRequestSerializer, UserBlockedFriendshipSerializer, UserFriendshipSerializer, FriendshipSerializer
from .models import FriendshipRequest, Friendship
from django.db.models import Q

class FriendshipRequestViewSet(viewsets.ModelViewSet):

    queryset = FriendshipRequest.objects.all()
    serializer_class = FriendshipRequestSerializer

class FriendshipViewSet(viewsets.ModelViewSet):

    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer

class UserFriendshipViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Friendship.objects.all()
    serializer_class = UserFriendshipSerializer

    def get_queryset(self):
        friendships = self.queryset.filter((Q(user_id=self.kwargs["pk"]) | Q(friend_id=self.kwargs["pk"])) & Q(status=Friendship.FriendshipStatusType.ACCEPTED))
        return friendships

class UserBlockViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Friendship.objects.all()
    serializer_class = UserBlockedFriendshipSerializer

    def get_queryset(self):
        return self.queryset.filter(Q(user_id=self.kwargs["pk"]) & Q(status=Friendship.FriendshipStatusType.BLOCKED))