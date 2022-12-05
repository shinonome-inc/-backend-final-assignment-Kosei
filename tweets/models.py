from django.db import models
from accounts.models import User


class Tweet(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
