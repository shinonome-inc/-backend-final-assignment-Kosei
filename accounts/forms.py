from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Friendship, User
from django.contrib.auth.forms import AuthenticationForm


class AccountsForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username")
        labels = {"username": "ユーザーID", "email": "メール"}


class LoginForm(AuthenticationForm):
    pass


class FollowForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = ("followee", "follower")
