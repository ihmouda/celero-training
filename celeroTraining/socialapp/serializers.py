from rest_framework import serializers
from .models import User, Friendship, FriendshipRequest
from django.db.models import Q

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'mobile_no']

class FriendshipRequestSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):

        # check if status update
        status = validated_data.get('status', None)
        if not instance.status == status:

            # Create friendship for accepted request
            if status == Friendship.FriendshipStatusType.ACCEPTED:

                friendship = Friendship(user=instance.user, friend=instance.friend)
                serializer = FriendshipSerializer(friendship)
                serializer.instance.save()

            validated_data['status'] = validated_data.get('status', instance.status)
            return super().update(instance, validated_data)

        return instance

    def create(self, validated_data):

        user = validated_data.get('user', None)
        friend = validated_data.get('friend', None)

        # check if user and fried are the same
        if user == friend:

            error = {'message': 'error same friendship request'}
            raise serializers.ValidationError(error)

        # check if already have requests or create one
        request = FriendshipRequest.objects.filter(user_id=user.id, friend_id=friend.id).first()
        if request is None:
            request = FriendshipRequest.objects.filter(user_id=friend.id, friend_id=user.id).first()
            if request is None:
                request = super().create(validated_data)

        # update the status to sent
        request.status = FriendshipRequest.FriendshipRequestStatusType.SENT
        request.save()
        return request

    class Meta:
        model = FriendshipRequest
        fields = '__all__'

class FriendshipSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):

        # check if status update
        status = validated_data.get('status', None)
        if instance.status != status:
            return super().update(instance, validated_data)

    def create(self, validated_data):

        user = validated_data.get('user', None)
        friend = validated_data.get('friend', None)

        # check if user and fried are the same
        if user == friend:
            error = {'message': 'error same user block'}
            raise serializers.ValidationError(error)
        if Friendship.objects.filter(Q(user_id=friend) & Q(friend_id=user)):
            error = {'message': 'error same user block'}
            raise serializers.ValidationError(error)

        # set the status
        validated_data['status'] = validated_data.get('status', Friendship.FriendshipStatusType.CANCELLED)
        return super().create(validated_data)

    class Meta:
        model = Friendship
        fields = '__all__'

class FriendRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return '(%d): %s' % (value.id, value.full_name)

class UserBlockedFriendshipSerializer(serializers.ModelSerializer):

    friend = FriendRelatedField(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'created_date', 'friend']

class UserFriendshipSerializer(FriendshipSerializer):

    user = FriendRelatedField(read_only=True)
    friend = FriendRelatedField(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'status', 'created_date', 'user', 'friend']