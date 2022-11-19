from django.contrib import admin

from .models import TweetModel


class TweetAdmin(admin.ModelAdmin):
    fields = ["author", "text", "created_date"]


admin.site.register(TweetModel, TweetAdmin)
