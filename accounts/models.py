from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    follower = models.ManyToManyField("self", through="Friendship", symmetrical=False)


class Friendship(models.Model):

    followee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendship_followee",
    )
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendship_follower",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["followee", "follower"], name="friendship_unique"
            ),
        ]
