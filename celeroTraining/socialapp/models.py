from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobile_no = models.CharField(max_length=12, null=True, blank=True)
    requests = models.ManyToManyField('self', through='FriendshipRequest')
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

class Friendship(models.Model):

    class FriendshipStatusType(models.TextChoices):
        CANCELLED = 'cancelled'
        ACCEPTED = 'accepted'
        REJECTED = 'rejected'
        BLOCKED = 'blocked'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    status = models.CharField(max_length=20, choices=FriendshipStatusType.choices, default=FriendshipStatusType.ACCEPTED)
    updated_date = models.DateTimeField(auto_now=True, verbose_name="updated date")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=" created date")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'friend'], name='unique constraint')
        ]