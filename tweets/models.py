from django.db import models
from django.conf import settings


class Tweet(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
