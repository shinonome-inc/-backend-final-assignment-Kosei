from django.conf import settings
from django.db import models


class Tweet(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    text = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    favorite = models.ManyToManyField("self", through="Favorite", symmetrical=False)


class Favorite(models.Model):
    tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, related_name="favorite_tweet"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorite_user"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tweet", "user"], name="favorite_unique"),
        ]
