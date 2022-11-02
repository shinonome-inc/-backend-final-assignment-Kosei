from django.contrib.auth.forms import UserCreationForm
from .models import User


class AccountsForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username")
        labels = {"username": "ユーザーID", "email": "メール"}
