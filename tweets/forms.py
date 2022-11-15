from .models import Tweet
from django import forms


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude = ["author"]
