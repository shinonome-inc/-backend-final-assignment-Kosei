from django.contrib import admin

from .models import Friendship, User


class UserAdmin(admin.ModelAdmin):
    fields = ["email", "username"]


admin.site.register(User, UserAdmin)


class FrienshipAdmin(admin.ModelAdmin):
    fileds = ["followee", "follower"]


admin.site.register(Friendship, FrienshipAdmin)
