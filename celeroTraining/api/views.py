from rest_framework import generics
from .serializers import UserSerializer, FriendshipSerializer, FriendshipRequestSerializer, BlockSerializer
from rest_framework.response import Response
from .models import User, Friendship, FriendshipRequest, Block

class CreateFriendshipRequest(generics.CreateAPIView):
    serializer_class = FriendshipRequestSerializer

class UpdateFriendshipRequest(generics.UpdateAPIView):
    queryset = FriendshipRequest.objects.all()
    serializer_class = FriendshipRequestSerializer

class CreateBlock(generics.CreateAPIView):
    serializer_class = BlockSerializer

class UpdateBlock(generics.UpdateAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

class UserFriends(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserBlocked(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer