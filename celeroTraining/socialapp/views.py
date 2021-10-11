from rest_framework import generics, viewsets
from .serializers import FriendshipRequestSerializer, BlockSerializer, UserBlockedSerializer, UserFriendshipSerializer
from .models import FriendshipRequest, Block, Friendship

class FriendshipRequestViewSet(viewsets.ModelViewSet):

    queryset = FriendshipRequest.objects.all()
    serializer_class = FriendshipRequestSerializer

class BlockViewSet(viewsets.ModelViewSet):

    queryset = Block.objects.all()
    serializer_class = BlockSerializer

class UserFriendshipViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserFriendshipSerializer

    def get_queryset(self):
        firstlist = Friendship.objects.filter(user_id=self.kwargs["pk"])
        secondlist = Friendship.objects.filter(friend_id=self.kwargs["pk"])

        return firstlist | secondlist

class UserBlockViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserBlockedSerializer

    def get_queryset(self):
        return Block.objects.filter(user_id=self.kwargs["pk"])