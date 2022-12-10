from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)


class Follow(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField("self", through="Friendship")


class Friendship(models.Model):

    followee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendship_followee"
    )
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendship_follower"
    )  #
