from django.contrib import admin

from .models import Tweet, Favorite


class TweetAdmin(admin.ModelAdmin):
    fields = [
        "author",
        "text",
    ]


admin.site.register(Tweet, TweetAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    fields = [
        "tweet",
        "user",
    ]


admin.site.register(Favorite, FavoriteAdmin)
