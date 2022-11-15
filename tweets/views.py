from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import TweetForm
from .models import Tweet
from django.urls import reverse_lazy


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"


class TweetCreateView(CreateView):
    template_name = "tweets/tweet.html"
    form_class = TweetForm
    model = Tweet
    success_url = reverse_lazy("tweets:home")
