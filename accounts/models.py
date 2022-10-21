from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32, validators=[MinLengthValidator(8)])


# class FriendShip(models.Model):
#     pass
