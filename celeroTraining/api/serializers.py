from rest_framework import serializers
from .models import User, Friendship, FriendshipRequest, Block
from django.contrib import auth


class AbstractUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'mobile_no']

class BlockSerializer(serializers.ModelSerializer):

    friend = AbstractUserSerializer()

    class Meta:
        model = Block
        fields = ['id', 'status', 'created_date', 'friend']

class FriendshipSerializer(serializers.ModelSerializer):

    friend = AbstractUserSerializer()

    class Meta:
        model = Friendship
        fields = ['id', 'status_date', 'friend']

class UserSerializer(AbstractUserSerializer):

    friendships = FriendshipSerializer(source='from_user', many=True, read_only=True)
    blocked = BlockSerializer(source='block_from_user', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'mobile_no', 'blocked', 'friendships']

class UserBlockedSerializer(UserSerializer):

    blocked = BlockSerializer(source='block_from_user', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['blocked']

class UserFrienshipSerializer(UserSerializer):

    friends = FriendshipSerializer(source='from_user', many=True, read_only=True)
    friends2 = FriendshipSerializer(source='to_user', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['friends', 'friends2']

class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = '__all__'