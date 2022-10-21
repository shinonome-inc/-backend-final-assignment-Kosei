from django import forms
from .models import User
from django.core.validators import MinLengthValidator


class AccountsForm(User):
    class Meta:
        model = User
        fields = ("email", "username", "password")
