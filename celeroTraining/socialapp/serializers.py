from rest_framework import serializers
from .models import User, Friendship, FriendshipRequest, Block
from rest_framework.response import Response
from django.utils.timezone import now

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'mobile_no']

class BlockSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):

        newStatus = validated_data.get('status', None)
        block = Block.objects.get(pk=instance.id)

        if block.status != newStatus:
            instance.save()

            if newStatus == 'active':
                friendship = Friendship(user=block.user, friend=block.friend, status="blocked")
                friendship.save()
            else:
                friendship = Friendship(user=block.user, friend=block.friend, status="cancelled")
                friendship.save()

    def create(self, validated_data):

        user = validated_data.get('user', None)
        friend = validated_data.get('friend', None)

        # check if user and fried are the same
        if user == friend:

            error = {'message': 'error same user block'}
            raise serializers.ValidationError(error)

        friendship = Friendship.objects.filter(user_id=user.id, friend_id=friend.id).first()
        if friendship is None:
            friendship = Friendship.objects.filter(user_id=friend.id, friend_id=user.id).first()
            if friendship is None:
                friendship = Friendship(user=user, friend=friend)

        friendship.status = 'blocked'
        friendship.save()

        return Block.objects.create(**validated_data)

    class Meta:
        model = Block
        fields = '__all__'

class FriendshipRequestSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):

        newStatus = validated_data.get('status', None)
        request = FriendshipRequest.objects.get(pk=instance.id)

        if request.status != newStatus:
            if newStatus == 'accepted':

                friendship = Friendship.objects.filter(user_id=instance.user.id, friend_id=instance.friend.id).first()
                if friendship is None:
                    friendship = Friendship.objects.filter(user_id=instance.friend.id, friend_id=instance.user.id).first()
                    if friendship is None:
                        friendship = Friendship(user=instance.user, friend=instance.friend)
                        friendship.save()

            instance.status = validated_data.get('status', instance.status)
            instance.save()
        return instance

    def create(self, validated_data):

        user = validated_data.get('user', None)
        friend = validated_data.get('friend', None)

        # check if user and fried are the same
        if user == friend:

            error = {'message': 'error same friendship request'}
            raise serializers.ValidationError(error)

        request = FriendshipRequest.objects.filter(user_id=user.id, friend_id=friend.id).first()
        if request is None:
            request = FriendshipRequest.objects.filter(user_id=friend.id, friend_id=user.id).first()
            if request is None:
                return FriendshipRequest.objects.create(**validated_data)

        if request.status == 'cancelled' or request.status == 'rejected':
            request.status = 'sent'
            request.save()
        else:

            error = {'message': 'request already sent'}
            raise serializers.ValidationError(error)

    class Meta:
        model = FriendshipRequest
        fields = '__all__'

class FriendshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friendship
        fields = '__all__'

class UserBlockedSerializer(BlockSerializer):

    friend = UserSerializer()

    class Meta:
        model = Block
        fields = ['id', 'status', 'created_date', 'friend']

class UserFriendshipSerializer(FriendshipSerializer):

    user = UserSerializer()
    friend = UserSerializer()

    class Meta:
        model = Block
        fields = ['id', 'status', 'created_date', 'user', 'friend']