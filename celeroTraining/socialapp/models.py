from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db.models import Q

from django.core.exceptions import ValidationError

class User(AbstractUser):
    mobile_no = models.CharField(max_length=12, null=True, blank=True)
    requests = models.ManyToManyField('self', through='FriendshipRequest')
    blocked = models.ManyToManyField('self', through='Block')
    friendships = models.ManyToManyField('self', through='Friendship')

    @property
    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

class FriendshipRequest(models.Model):

    class FriendshipRequestStatusType(models.TextChoices):
        SENT = 'sent'
        ACCEPTED = 'accepted'
        CANCELLED = 'cancelled'
        REJECTED = 'rejected'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_from_user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_to_user")
    status = models.CharField(max_length=20, choices=FriendshipRequestStatusType.choices, default=FriendshipRequestStatusType.SENT, verbose_name="friendship request status")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="first created date", editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'friend'], name='request unique constraint')
        ]

class Block(models.Model):

    class BlockStatusType(models.TextChoices):
        ACTIVE = 'active'
        INACTIVE = 'inactive'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="block_from_user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="block_to_user")
    status = models.CharField(max_length=20, choices=BlockStatusType.choices, default=BlockStatusType.ACTIVE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="first created date", editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'friend'], name='block unique constraint')
        ]

class Friendship(models.Model):

    class FriendshipStatusType(models.TextChoices):
        CANCELLED = 'cancelled'
        ACCEPTED = 'accepted'
        REJECTED = 'rejected'
        BLOCKED = 'blocked'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    status = models.CharField(max_length=20, choices=FriendshipStatusType.choices, default=FriendshipStatusType.ACCEPTED)
    status_date = models.DateTimeField(auto_now_add=True, verbose_name="status change date")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="first created date")

    def save(self, *args, **kwargs):
        if self.pk is not None:
            friendship = Friendship.objects.get(pk=self.pk)
            if friendship.status != self.status:
                self.status_date = now()
            super().save(*args, **kwargs)

        if self.user.pk == self.friend.pk:
            raise ValueError("error same user")
        elif Friendship.objects.filter(Q(user_id=self.friend.id) & Q(friend_id=self.user.id)):
            raise ValueError("error same friendship")
        else:
            super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'friend'], name='unique constraint')
        ]