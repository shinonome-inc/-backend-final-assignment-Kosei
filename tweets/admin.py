from django.contrib import admin

from .models import Tweet


class TweetAdmin(admin.ModelAdmin):
    fields = [
        "author",
        "text",
    ]


admin.site.register(Tweet, TweetAdmin)
