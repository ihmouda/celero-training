from rest_framework import serializers
from .models import User, Friendship, FriendshipRequest, Block
from django.contrib import auth


class FakeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'mobile_no']

class BlockSerializer(serializers.ModelSerializer):

    # block_from_user = FakeUserSerializer()
    # block_to_user = FakeUserSerializer()

    class Meta:
        model = Block
        fields = ['id', 'status', 'created_date']

class FriendshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friendship
        fields = ['id', 'status_date']

class UserSerializer(serializers.ModelSerializer):

    friendships = FriendshipSerializer(many=True, read_only=True)
    blocked = BlockSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'mobile_no', 'blocked']

class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = '__all__'