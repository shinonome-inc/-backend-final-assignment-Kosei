from django.db import models
from accounts.models import User


class Tweet(models.Model):
    author = models.ForeignKey(
        User,
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
        User, on_delete=models.CASCADE, related_name="favorite_user"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tweet", "user"], name="favorite_unique"),
        ]
