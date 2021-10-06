from django.contrib import admin
from .models import User, Friendship, FriendshipRequest, Block

admin.site.register(User)
admin.site.register(Friendship)
admin.site.register(FriendshipRequest)
admin.site.register(Block)

